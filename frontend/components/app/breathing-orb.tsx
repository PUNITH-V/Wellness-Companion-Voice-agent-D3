'use client';

import { cn } from '@/lib/utils';

interface BreathingOrbProps {
  state?: 'idle' | 'listening' | 'thinking' | 'speaking';
  className?: string;
}

export function BreathingOrb({ state = 'idle', className }: BreathingOrbProps) {
  return (
    <div className={cn('relative flex items-center justify-center', className)}>
      {/* Outer ripple rings */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div
          className={cn(
            'absolute h-full w-full rounded-full border border-primary/20',
            'animate-ripple-1'
          )}
        />
        <div
          className={cn(
            'absolute h-full w-full rounded-full border border-primary/15',
            'animate-ripple-2'
          )}
        />
        <div
          className={cn(
            'absolute h-full w-full rounded-full border border-primary/10',
            'animate-ripple-3'
          )}
        />
      </div>

      {/* Main breathing orb */}
      <div
        className={cn(
          'relative z-10 h-32 w-32 rounded-full transition-all duration-1000',
          'animate-fluid-breathe',
          state === 'listening' && 'scale-110 animate-pulse-fast',
          state === 'thinking' && 'animate-pulse-medium',
          state === 'speaking' && 'scale-105 animate-pulse-fast'
        )}
        style={{
          background: 'linear-gradient(135deg, #a8c5b8 0%, #84a98c 50%, #6b9080 100%)',
          boxShadow: `
            0 0 60px rgba(132, 169, 140, 0.4),
            inset 10px 10px 40px rgba(255, 255, 255, 0.3),
            inset -10px -10px 40px rgba(107, 144, 128, 0.3)
          `,
        }}
      >
        {/* Inner highlight for 3D effect */}
        <div
          className="absolute left-[25%] top-[20%] h-10 w-10 rounded-full opacity-40 blur-xl"
          style={{
            background: 'rgba(255, 255, 255, 0.6)',
          }}
        />

        {/* Center glow */}
        <div
          className="absolute inset-0 rounded-full opacity-50 blur-2xl"
          style={{
            background: 'radial-gradient(circle, rgba(168, 197, 184, 0.8) 0%, transparent 70%)',
          }}
        />
      </div>

      {/* State indicator text */}
      {state !== 'idle' && (
        <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 text-xs text-muted-foreground">
          {state === 'listening' && 'Listening...'}
          {state === 'thinking' && 'Thinking...'}
          {state === 'speaking' && 'Speaking...'}
        </div>
      )}

      <style jsx>{`
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

        @keyframes ripple-1 {
          0% {
            transform: scale(1);
            opacity: 0.4;
          }
          100% {
            transform: scale(1.4);
            opacity: 0;
          }
        }

        @keyframes ripple-2 {
          0% {
            transform: scale(1);
            opacity: 0.3;
          }
          100% {
            transform: scale(1.6);
            opacity: 0;
          }
        }

        @keyframes ripple-3 {
          0% {
            transform: scale(1);
            opacity: 0.2;
          }
          100% {
            transform: scale(1.8);
            opacity: 0;
          }
        }

        @keyframes pulse-fast {
          0%,
          100% {
            opacity: 1;
          }
          50% {
            opacity: 0.8;
          }
        }

        @keyframes pulse-medium {
          0%,
          100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.9;
            transform: scale(1.02);
          }
        }

        .animate-fluid-breathe {
          animation: fluid-breathe 6s ease-in-out infinite;
        }

        .animate-ripple-1 {
          animation: ripple-1 3s ease-out infinite;
        }

        .animate-ripple-2 {
          animation: ripple-2 3s ease-out infinite 1s;
        }

        .animate-ripple-3 {
          animation: ripple-3 3s ease-out infinite 2s;
        }

        .animate-pulse-fast {
          animation: pulse-fast 1s ease-in-out infinite;
        }

        .animate-pulse-medium {
          animation: pulse-medium 2s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}
