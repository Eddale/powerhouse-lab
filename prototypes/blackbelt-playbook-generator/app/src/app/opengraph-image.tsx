import { ImageResponse } from 'next/og';

export const runtime = 'edge';

export const alt = 'Playbook Generator | BlackBelt - Generate professional onboarding playbooks for any role in 30 seconds';
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = 'image/png';

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#000000',
          backgroundImage: 'radial-gradient(circle at 25% 25%, #1a1a1a 0%, #000000 50%)',
        }}
      >
        {/* Gold accent bar at top */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '8px',
            backgroundColor: '#EFBB39',
          }}
        />

        {/* BlackBelt text logo */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '40px',
          }}
        >
          <div
            style={{
              fontSize: '48px',
              fontWeight: 900,
              color: '#FFFFFF',
              letterSpacing: '-1px',
            }}
          >
            BLACK
          </div>
          <div
            style={{
              fontSize: '48px',
              fontWeight: 900,
              color: '#EFBB39',
              letterSpacing: '-1px',
            }}
          >
            BELT
          </div>
        </div>

        {/* Main title */}
        <div
          style={{
            fontSize: '72px',
            fontWeight: 800,
            color: '#FFFFFF',
            textAlign: 'center',
            marginBottom: '24px',
            lineHeight: 1.1,
          }}
        >
          Playbook Generator
        </div>

        {/* Subtitle */}
        <div
          style={{
            fontSize: '32px',
            fontWeight: 500,
            color: '#888888',
            textAlign: 'center',
            maxWidth: '900px',
          }}
        >
          Generate professional onboarding playbooks for any role in 30 seconds
        </div>

        {/* Gold accent bar at bottom */}
        <div
          style={{
            position: 'absolute',
            bottom: '60px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
          }}
        >
          <div
            style={{
              width: '60px',
              height: '4px',
              backgroundColor: '#EFBB39',
            }}
          />
          <div
            style={{
              fontSize: '20px',
              fontWeight: 600,
              color: '#666666',
              textTransform: 'uppercase',
              letterSpacing: '2px',
            }}
          >
            Built for coaches who ship
          </div>
          <div
            style={{
              width: '60px',
              height: '4px',
              backgroundColor: '#EFBB39',
            }}
          />
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
