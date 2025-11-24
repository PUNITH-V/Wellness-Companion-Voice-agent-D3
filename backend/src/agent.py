import logging
import json
import os
from datetime import datetime
from pathlib import Path
import aiohttp

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")
load_dotenv(".env")

# Path to wellness log file
WELLNESS_LOG_PATH = Path("wellness_log.json")

# Notion API configuration
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN", "")
NOTION_WELLNESS_DB_ID = os.getenv("NOTION_WELLNESS_DB_ID", "")
NOTION_TODO_DB_ID = os.getenv("NOTION_TODO_DB_ID", "")
NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def load_wellness_history():
    """Load previous wellness check-ins from JSON file"""
    if WELLNESS_LOG_PATH.exists():
        with open(WELLNESS_LOG_PATH, 'r') as f:
            return json.load(f)
    return []


def save_wellness_entry(entry):
    """Save a wellness check-in entry to JSON file"""
    history = load_wellness_history()
    history.append(entry)
    with open(WELLNESS_LOG_PATH, 'w') as f:
        json.dump(history, f, indent=2)
    logger.info(f"Saved wellness entry: {entry}")


def get_context_from_history():
    """Generate context string from previous check-ins"""
    history = load_wellness_history()
    if not history:
        return "This is the user's first check-in."
    
    last_entry = history[-1]
    context = f"Last check-in was on {last_entry['date']}. "
    context += f"Their mood was: {last_entry['mood']}. "
    if last_entry.get('objectives'):
        context += f"They wanted to: {', '.join(last_entry['objectives'])}."
    
    return context


class Assistant(Agent):
    def __init__(self) -> None:
        history_context = get_context_from_history()
        
        super().__init__(
            instructions=f"""You are a supportive health and wellness voice companion. The user is interacting with you via voice.

Your role is to conduct a brief daily check-in:
1. Ask about their mood and energy level today
2. Ask what's stressing them or what they're feeling
3. Ask about 1-3 things they'd like to accomplish today
4. Offer simple, practical, grounded advice (no medical diagnosis)
5. Close with a brief recap of their mood and objectives

Keep responses:
- Warm, supportive, and non-judgmental
- Concise and conversational
- Free of complex formatting, emojis, or asterisks
- Grounded and realistic (suggest small actionable steps)

Previous context: {history_context}

Reference their previous check-in naturally in conversation if relevant.

You also have access to a Notion-based todo list system. You can:
- Create tasks when users want to add items to their todo list
- View their current tasks when they ask what they need to do
- Mark tasks as complete when they finish them
- Update task details when they want to modify a task
- Delete tasks when they want to remove them

Use these tools naturally when the user mentions tasks, todos, or things they need to do.""",
        )

    @function_tool
    async def save_checkin(
        self,
        context: RunContext,
        mood: str,
        objectives: str,
        summary: str = ""
    ):
        """Save the daily wellness check-in data to both JSON and Notion.
        
        Call this tool at the end of the conversation to persist the check-in data.
        
        Args:
            mood: User's self-reported mood and energy level
            objectives: Comma-separated list of 1-3 things they want to accomplish
            summary: Brief summary of the conversation
        """
        entry = {
            "date": datetime.now().isoformat(),
            "mood": mood,
            "objectives": [obj.strip() for obj in objectives.split(",")],
            "summary": summary
        }
        
        # Save to local JSON
        save_wellness_entry(entry)
        
        # Save to Notion if configured
        if NOTION_API_TOKEN and NOTION_WELLNESS_DB_ID:
            try:
                await self._save_to_notion(entry)
                return f"Check-in saved to both local storage and Notion! Your mood: {mood}. Objectives: {objectives}"
            except Exception as e:
                logger.error(f"Error saving to Notion: {str(e)}")
                return f"Check-in saved locally! Your mood: {mood}. Objectives: {objectives}"
        
        return f"Check-in saved! Your mood: {mood}. Objectives: {objectives}"
    
    async def _save_to_notion(self, entry: dict):
        """Helper method to save check-in to Notion database"""
        objectives_list = entry['objectives']
        
        # Create page in Notion database
        page_data = {
            "parent": {"database_id": NOTION_WELLNESS_DB_ID},
            "properties": {
                "Date": {
                    "date": {
                        "start": entry['date']
                    }
                },
                "Mood": {
                    "rich_text": [
                        {
                            "text": {
                                "content": entry['mood']
                            }
                        }
                    ]
                },
                "Objectives": {
                    "rich_text": [
                        {
                            "text": {
                                "content": ", ".join(objectives_list)
                            }
                        }
                    ]
                },
                "Summary": {
                    "rich_text": [
                        {
                            "text": {
                                "content": entry.get('summary', '')
                            }
                        }
                    ]
                }
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{NOTION_API_URL}/pages",
                headers={
                    "Authorization": f"Bearer {NOTION_API_TOKEN}",
                    "Content-Type": "application/json",
                    "Notion-Version": NOTION_VERSION
                },
                json=page_data
            ) as response:
                if response.status == 200:
                    logger.info(f"Saved check-in to Notion: {entry['date']}")
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to save to Notion: {response.status} - {error_text}")
                    raise Exception(f"Notion API error: {response.status}")
    
    @function_tool
    async def create_todo_tasks(
        self,
        context: RunContext,
        tasks: str
    ):
        """Create tasks in Notion todo list from user's goals or objectives.
        
        Use this when the user explicitly wants to turn their goals into tasks,
        or says things like "add these to my todo list" or "create tasks for these".
        
        Args:
            tasks: Comma-separated list of tasks to create
        """
        if not NOTION_API_TOKEN or not NOTION_TODO_DB_ID:
            return "Todo list is not configured. Please set up your Notion todo database."
        
        task_list = [task.strip() for task in tasks.split(",")]
        created_tasks = []
        
        async with aiohttp.ClientSession() as session:
            for task_content in task_list:
                try:
                    page_data = {
                        "parent": {"database_id": NOTION_TODO_DB_ID},
                        "properties": {
                            "Task": {
                                "title": [
                                    {
                                        "text": {
                                            "content": task_content
                                        }
                                    }
                                ]
                            },
                            "Status": {
                                "status": {
                                    "name": "Not started"
                                }
                            },
                            "Date": {
                                "date": {
                                    "start": datetime.now().isoformat()
                                }
                            }
                        }
                    }
                    
                    async with session.post(
                        f"{NOTION_API_URL}/pages",
                        headers={
                            "Authorization": f"Bearer {NOTION_API_TOKEN}",
                            "Content-Type": "application/json",
                            "Notion-Version": NOTION_VERSION
                        },
                        json=page_data
                    ) as response:
                        if response.status == 200:
                            created_tasks.append(task_content)
                            logger.info(f"Created Notion task: {task_content}")
                        else:
                            error_text = await response.text()
                            logger.error(f"Failed to create task: {task_content}, Status: {response.status} - {error_text}")
                except Exception as e:
                    logger.error(f"Error creating task {task_content}: {str(e)}")
        
        if created_tasks:
            return f"Created {len(created_tasks)} task(s) in your Notion todo list: {', '.join(created_tasks)}"
        else:
            return "Sorry, I couldn't create the tasks. Please try again."
    
    @function_tool
    async def get_todo_tasks(
        self,
        context: RunContext
    ):
        """Get tasks from Notion todo list.
        
        Use this when the user asks to see their tasks, todo list, or what they need to do.
        """
        if not NOTION_API_TOKEN or not NOTION_TODO_DB_ID:
            return "Todo list is not configured. Please set up your Notion todo database."
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NOTION_API_URL}/databases/{NOTION_TODO_DB_ID}/query",
                    headers={
                        "Authorization": f"Bearer {NOTION_API_TOKEN}",
                        "Content-Type": "application/json",
                        "Notion-Version": NOTION_VERSION
                    },
                    json={
                        "filter": {
                            "property": "Status",
                            "status": {
                                "does_not_equal": "Done"
                            }
                        },
                        "sorts": [
                            {
                                "property": "Date",
                                "direction": "descending"
                            }
                        ]
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        tasks = data.get("results", [])
                        
                        if not tasks:
                            return "You don't have any pending tasks in your todo list right now."
                        
                        task_list = []
                        for task in tasks[:10]:  # Limit to 10 tasks
                            task_name = task["properties"]["Task"]["title"][0]["text"]["content"]
                            status = task["properties"]["Status"]["status"]["name"]
                            task_list.append(f"- {task_name} ({status})")
                        
                        return f"Here are your tasks:\n" + "\n".join(task_list)
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to get tasks: {response.status} - {error_text}")
                        return "Sorry, I couldn't retrieve your tasks."
        except Exception as e:
            logger.error(f"Error getting Notion tasks: {str(e)}")
            return "Sorry, I encountered an error retrieving your tasks."
    
    @function_tool
    async def complete_todo_task(
        self,
        context: RunContext,
        task_name: str
    ):
        """Mark a task as complete in Notion todo list.
        
        Use this when the user says they completed a task or wants to mark something as done.
        
        Args:
            task_name: The name of the task to mark as complete
        """
        if not NOTION_API_TOKEN or not NOTION_TODO_DB_ID:
            return "Todo list is not configured. Please set up your Notion todo database."
        
        try:
            # First, get all tasks to find the matching one
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NOTION_API_URL}/databases/{NOTION_TODO_DB_ID}/query",
                    headers={
                        "Authorization": f"Bearer {NOTION_API_TOKEN}",
                        "Content-Type": "application/json",
                        "Notion-Version": NOTION_VERSION
                    },
                    json={}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        tasks = data.get("results", [])
                        
                        # Find task by name (case-insensitive partial match)
                        matching_task = None
                        for task in tasks:
                            task_title = task["properties"]["Task"]["title"][0]["text"]["content"]
                            if task_name.lower() in task_title.lower():
                                matching_task = task
                                break
                        
                        if not matching_task:
                            return f"I couldn't find a task matching '{task_name}' in your todo list."
                        
                        # Update the task status to Done
                        async with session.patch(
                            f"{NOTION_API_URL}/pages/{matching_task['id']}",
                            headers={
                                "Authorization": f"Bearer {NOTION_API_TOKEN}",
                                "Content-Type": "application/json",
                                "Notion-Version": NOTION_VERSION
                            },
                            json={
                                "properties": {
                                    "Status": {
                                        "status": {
                                            "name": "Done"
                                        }
                                    }
                                }
                            }
                        ) as update_response:
                            if update_response.status == 200:
                                task_title = matching_task["properties"]["Task"]["title"][0]["text"]["content"]
                                logger.info(f"Completed Notion task: {task_title}")
                                return f"Great! I've marked '{task_title}' as complete."
                            else:
                                return f"Sorry, I couldn't complete the task '{task_name}'."
                    else:
                        return "Sorry, I couldn't access your todo list."
        except Exception as e:
            logger.error(f"Error completing Notion task: {str(e)}")
            return "Sorry, I encountered an error completing the task."
    
    @function_tool
    async def update_todo_task(
        self,
        context: RunContext,
        task_name: str,
        new_task_name: str = "",
        new_status: str = ""
    ):
        """Update a task in Notion todo list.
        
        Use this when the user wants to rename a task or change its status.
        
        Args:
            task_name: The current name of the task to update
            new_task_name: The new name for the task (optional)
            new_status: The new status (e.g., "In progress", "Not started", "Done") (optional)
        """
        if not NOTION_API_TOKEN or not NOTION_TODO_DB_ID:
            return "Todo list is not configured. Please set up your Notion todo database."
        
        if not new_task_name and not new_status:
            return "Please specify what you'd like to update - the task name or status."
        
        try:
            # First, get all tasks to find the matching one
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NOTION_API_URL}/databases/{NOTION_TODO_DB_ID}/query",
                    headers={
                        "Authorization": f"Bearer {NOTION_API_TOKEN}",
                        "Content-Type": "application/json",
                        "Notion-Version": NOTION_VERSION
                    },
                    json={}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        tasks = data.get("results", [])
                        
                        # Find task by name (case-insensitive partial match)
                        matching_task = None
                        for task in tasks:
                            task_title = task["properties"]["Task"]["title"][0]["text"]["content"]
                            if task_name.lower() in task_title.lower():
                                matching_task = task
                                break
                        
                        if not matching_task:
                            return f"I couldn't find a task matching '{task_name}' in your todo list."
                        
                        # Build update payload
                        update_properties = {}
                        
                        if new_task_name:
                            update_properties["Task"] = {
                                "title": [
                                    {
                                        "text": {
                                            "content": new_task_name
                                        }
                                    }
                                ]
                            }
                        
                        if new_status:
                            update_properties["Status"] = {
                                "status": {
                                    "name": new_status
                                }
                            }
                        
                        # Update the task
                        async with session.patch(
                            f"{NOTION_API_URL}/pages/{matching_task['id']}",
                            headers={
                                "Authorization": f"Bearer {NOTION_API_TOKEN}",
                                "Content-Type": "application/json",
                                "Notion-Version": NOTION_VERSION
                            },
                            json={
                                "properties": update_properties
                            }
                        ) as update_response:
                            if update_response.status == 200:
                                old_title = matching_task["properties"]["Task"]["title"][0]["text"]["content"]
                                logger.info(f"Updated Notion task: {old_title}")
                                
                                update_msg = f"I've updated the task '{old_title}'"
                                if new_task_name:
                                    update_msg += f" to '{new_task_name}'"
                                if new_status:
                                    update_msg += f" with status '{new_status}'"
                                return update_msg + "."
                            else:
                                return f"Sorry, I couldn't update the task '{task_name}'."
                    else:
                        return "Sorry, I couldn't access your todo list."
        except Exception as e:
            logger.error(f"Error updating Notion task: {str(e)}")
            return "Sorry, I encountered an error updating the task."
    
    @function_tool
    async def delete_todo_task(
        self,
        context: RunContext,
        task_name: str
    ):
        """Delete a task from Notion todo list.
        
        Use this when the user wants to remove or delete a task.
        
        Args:
            task_name: The name of the task to delete
        """
        if not NOTION_API_TOKEN or not NOTION_TODO_DB_ID:
            return "Todo list is not configured. Please set up your Notion todo database."
        
        try:
            # First, get all tasks to find the matching one
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NOTION_API_URL}/databases/{NOTION_TODO_DB_ID}/query",
                    headers={
                        "Authorization": f"Bearer {NOTION_API_TOKEN}",
                        "Content-Type": "application/json",
                        "Notion-Version": NOTION_VERSION
                    },
                    json={}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        tasks = data.get("results", [])
                        
                        # Find task by name (case-insensitive partial match)
                        matching_task = None
                        for task in tasks:
                            task_title = task["properties"]["Task"]["title"][0]["text"]["content"]
                            if task_name.lower() in task_title.lower():
                                matching_task = task
                                break
                        
                        if not matching_task:
                            return f"I couldn't find a task matching '{task_name}' in your todo list."
                        
                        # Archive (delete) the task by setting archived to true
                        async with session.patch(
                            f"{NOTION_API_URL}/pages/{matching_task['id']}",
                            headers={
                                "Authorization": f"Bearer {NOTION_API_TOKEN}",
                                "Content-Type": "application/json",
                                "Notion-Version": NOTION_VERSION
                            },
                            json={
                                "archived": True
                            }
                        ) as delete_response:
                            if delete_response.status == 200:
                                task_title = matching_task["properties"]["Task"]["title"][0]["text"]["content"]
                                logger.info(f"Deleted Notion task: {task_title}")
                                return f"I've deleted the task '{task_title}' from your todo list."
                            else:
                                return f"Sorry, I couldn't delete the task '{task_name}'."
                    else:
                        return "Sorry, I couldn't access your todo list."
        except Exception as e:
            logger.error(f"Error deleting Notion task: {str(e)}")
            return "Sorry, I encountered an error deleting the task."


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
