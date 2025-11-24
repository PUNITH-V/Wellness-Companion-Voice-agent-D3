'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/livekit/button';

function FloatingLeaf({ delay = 0, duration = 20 }: { delay?: number; duration?: number }) {
  return (
    <div
      className="absolute opacity-20"
      style={{
        animation: `float-leaf ${duration}s ease-in-out infinite`,
        animationDelay: `${delay}s`,
      }}
    >
      <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" className="text-primary">
        <path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z" />
      </svg>
    </div>
  );
}

function BreathingCircle({ size = 'md', delay = 0 }: { size?: 'sm' | 'md' | 'lg'; delay?: number }) {
  const sizeClasses = {
    sm: 'h-40 w-40',
    md: 'h-56 w-56',
    lg: 'h-72 w-72',
  };

  return (
    <div
      className={`absolute rounded-full border-2 border-primary/10 ${sizeClasses[size]}`}
      style={{
        animation: 'breathe-circle 8s ease-in-out infinite',
        animationDelay: `${delay}s`,
      }}
    />
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  const [currentTime, setCurrentTime] = useState('');
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = now.getHours();
      
      // Set greeting based on time
      if (hours < 12) setGreeting('Good Morning');
      else if (hours < 17) setGreeting('Good Afternoon');
      else setGreeting('Good Evening');
      
      // Format time
      setCurrentTime(now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
      }));
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div ref={ref} className="animated-bg relative flex min-h-screen items-center justify-center overflow-hidden px-4">
      {/* Floating Leaves */}
      <div className="pointer-events-none absolute inset-0">
        <FloatingLeaf delay={0} duration={25} />
        <FloatingLeaf delay={5} duration={30} />
        <FloatingLeaf delay={10} duration={22} />
        <FloatingLeaf delay={15} duration={28} />
      </div>

      {/* Breathing Circles Background */}
      <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <BreathingCircle size="lg" delay={0} />
        <BreathingCircle size="md" delay={2} />
        <BreathingCircle size="sm" delay={4} />
      </div>

      {/* Main Content */}
      <div className="animate-fade-in-up relative z-10 w-full max-w-2xl px-4 text-center">
        {/* Time Display */}
        <div className="mb-6 flex flex-col items-center gap-2">
          <div className="text-4xl font-extralight tracking-tight text-foreground sm:text-5xl md:text-6xl">
            {currentTime}
          </div>
          <div className="text-base font-light text-muted-foreground sm:text-lg md:text-xl">
            {greeting}
          </div>
        </div>

        {/* Central Orb */}
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div
              className="h-32 w-32 rounded-full sm:h-36 sm:w-36 md:h-40 md:w-40"
              style={{
                background: 'linear-gradient(135deg, #a8c5b8 0%, #84a98c 50%, #6b9080 100%)',
                boxShadow: '0 0 60px rgba(132, 169, 140, 0.4), inset 10px 10px 40px rgba(255, 255, 255, 0.3)',
                animation: 'fluid-breathe 6s ease-in-out infinite',
              }}
            >
              {/* Inner glow */}
              <div
                className="absolute left-[25%] top-[20%] h-10 w-10 rounded-full opacity-40 blur-xl"
                style={{ background: 'rgba(255, 255, 255, 0.6)' }}
              />
            </div>
            
            {/* Pulse rings */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="absolute h-full w-full animate-ping-slow rounded-full border-2 border-primary/20" />
            </div>
          </div>
        </div>

        {/* Main Message */}
        <h1 className="mb-4 text-2xl font-light leading-relaxed text-foreground sm:text-3xl md:text-4xl lg:text-5xl">
          The space is yours.
          <br />
          <span className="text-primary">How is your energy flowing?</span>
        </h1>

        <p className="mb-10 text-base text-muted-foreground/80 sm:text-lg md:text-xl">
          Take a moment to check in with yourself
        </p>

        {/* Start Button */}
        <Button
          variant="primary"
          size="lg"
          onClick={onStartCall}
          className="group relative overflow-hidden rounded-full bg-primary px-10 py-5 text-lg font-medium text-primary-foreground shadow-lg transition-all hover:scale-105 hover:shadow-xl active:scale-95 sm:px-12 sm:py-6 sm:text-xl"
        >
          <span className="relative z-10 flex items-center gap-3">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
            </svg>
            {startButtonText}
          </span>
          <div className="absolute inset-0 -z-0 bg-gradient-to-r from-accent to-primary opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
        </Button>

        {/* Feature Pills */}
        <div className="mt-12 flex flex-wrap items-center justify-center gap-3">
          {[
            { icon: '🌿', label: 'Mindful' },
            { icon: '✨', label: 'Intentions' },
            { icon: '💚', label: 'Guidance' },
          ].map((feature, i) => (
            <div
              key={i}
              className="flex items-center gap-2 rounded-full border border-border bg-card/80 px-4 py-3 text-sm backdrop-blur-sm transition-all hover:scale-105 hover:bg-card sm:gap-2.5 sm:px-5 sm:py-3.5 sm:text-base"
            >
              <span className="text-xl sm:text-2xl">{feature.icon}</span>
              <span className="font-medium text-foreground">{feature.label}</span>
            </div>
          ))}
        </div>

        {/* Bottom Info */}
        <div className="mt-12 flex items-center justify-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 animate-pulse rounded-full bg-green-500" />
            <span>Secure</span>
          </div>
          <div className="h-1 w-1 rounded-full bg-muted-foreground/40" />
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 animate-pulse rounded-full bg-primary" />
            <span>AI-Powered</span>
          </div>
        </div>
      </div>

      {/* Ambient Glow Effects */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/4 left-1/4 h-96 w-96 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute -bottom-1/4 right-1/4 h-96 w-96 rounded-full bg-accent/10 blur-3xl" />
      </div>

      <style jsx>{`
        @keyframes float-leaf {
          0% {
            transform: translate(0, 0) rotate(0deg);
            opacity: 0;
          }
          10% {
            opacity: 0.2;
          }
          90% {
            opacity: 0.2;
          }
          100% {
            transform: translate(100vw, 100vh) rotate(360deg);
            opacity: 0;
          }
        }

        @keyframes breathe-circle {
          0%, 100% {
            transform: scale(1);
            opacity: 0.1;
          }
          50% {
            transform: scale(1.2);
            opacity: 0.05;
          }
        }

        @keyframes fluid-breathe {
          0% {
            border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
            transform: scale(1);
          }
          50% {
            border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
            transform: scale(1.05);
          }
          100% {
            border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
            transform: scale(1);
          }
        }

        @keyframes ping-slow {
          0% {
            transform: scale(1);
            opacity: 0.3;
          }
          50% {
            transform: scale(1.1);
            opacity: 0.1;
          }
          100% {
            transform: scale(1);
            opacity: 0.3;
          }
        }

        .animate-ping-slow {
          animation: ping-slow 3s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};
