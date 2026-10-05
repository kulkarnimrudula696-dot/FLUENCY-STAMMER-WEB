/**
 * FLUENCY Avatar Engine
 * Curated, friendly, simple illustrated vector avatars for user profiles.
 * Designed for warm aesthetics, zero photographic dependencies, and crisp SVG scaling.
 */

const AvatarEngine = {
  avatars: [
    {
      id: 'avatar-sunny',
      name: 'Sunny',
      tagline: 'Warm & Cheerful',
      bg: '#FFF8E1',
      border: '#FFE082',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#FFF8E1" stroke="#FFE082" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 24 95 Q 50 78 76 95 Z" fill="#FFB74D"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#F5CBA7"/>
          <!-- Head -->
          <ellipse cx="50" cy="50" rx="22" ry="24" fill="#FADBD8"/>
          <!-- Hair (Curly Honey) -->
          <circle cx="34" cy="36" r="10" fill="#78350F"/>
          <circle cx="66" cy="36" r="10" fill="#78350F"/>
          <circle cx="50" cy="30" r="12" fill="#78350F"/>
          <circle cx="40" cy="30" r="10" fill="#78350F"/>
          <circle cx="60" cy="30" r="10" fill="#78350F"/>
          <!-- Eyes -->
          <circle cx="42" cy="50" r="3" fill="#3D2B24"/>
          <circle cx="58" cy="50" r="3" fill="#3D2B24"/>
          <circle cx="43" cy="49" r="1" fill="#FFFFFF"/>
          <circle cx="59" cy="49" r="1" fill="#FFFFFF"/>
          <!-- Cheeks -->
          <circle cx="37" cy="56" r="4" fill="#F1948A" opacity="0.6"/>
          <circle cx="63" cy="56" r="4" fill="#F1948A" opacity="0.6"/>
          <!-- Smile -->
          <path d="M 44 58 Q 50 66 56 58" fill="none" stroke="#3D2B24" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-breeze',
      name: 'Breeze',
      tagline: 'Calm & Steady',
      bg: '#E8F5E9',
      border: '#A5D6A7',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#E8F5E9" stroke="#A5D6A7" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#66BB6A"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#F5CBA7"/>
          <!-- Head -->
          <ellipse cx="50" cy="50" rx="22" ry="24" fill="#FDEBD0"/>
          <!-- Hair (Sleek Dark) -->
          <path d="M 28 44 C 28 26, 72 26, 72 44 C 70 30, 30 30, 28 44 Z" fill="#2C3E50"/>
          <path d="M 28 44 Q 30 32 46 32 Q 54 36 68 40" fill="none" stroke="#2C3E50" stroke-width="7" stroke-linecap="round"/>
          <!-- Eyes -->
          <ellipse cx="42" cy="51" rx="3.5" ry="3" fill="#2C3E50"/>
          <ellipse cx="58" cy="51" rx="3.5" ry="3" fill="#2C3E50"/>
          <circle cx="43" cy="50" r="1" fill="#FFFFFF"/>
          <circle cx="59" cy="50" r="1" fill="#FFFFFF"/>
          <!-- Eyebrows -->
          <path d="M 38 45 Q 42 43 46 45" fill="none" stroke="#2C3E50" stroke-width="1.8" stroke-linecap="round"/>
          <path d="M 54 45 Q 58 43 62 45" fill="none" stroke="#2C3E50" stroke-width="1.8" stroke-linecap="round"/>
          <!-- Cheeks -->
          <circle cx="36" cy="56" r="3.5" fill="#81C784" opacity="0.45"/>
          <circle cx="64" cy="56" r="3.5" fill="#81C784" opacity="0.45"/>
          <!-- Smile -->
          <path d="M 44 59 Q 50 67 56 59" fill="none" stroke="#2C3E50" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-spark',
      name: 'Spark',
      tagline: 'Bright & Focused',
      bg: '#FFEBE6',
      border: '#FFAB91',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#FFEBE6" stroke="#FFAB91" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#FF7043"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#EDBB99"/>
          <!-- Head -->
          <ellipse cx="50" cy="50" rx="22" ry="24" fill="#F5CBA7"/>
          <!-- Hair (Voluminous Afro/Curl) -->
          <circle cx="30" cy="40" r="12" fill="#4A235A"/>
          <circle cx="70" cy="40" r="12" fill="#4A235A"/>
          <circle cx="50" cy="28" r="14" fill="#4A235A"/>
          <circle cx="38" cy="30" r="12" fill="#4A235A"/>
          <circle cx="62" cy="30" r="12" fill="#4A235A"/>
          <!-- Round Glasses -->
          <circle cx="41" cy="50" r="8" fill="none" stroke="#D35400" stroke-width="2.5"/>
          <circle cx="59" cy="50" r="8" fill="none" stroke="#D35400" stroke-width="2.5"/>
          <line x1="49" y1="50" x2="51" y2="50" stroke="#D35400" stroke-width="2.5"/>
          <!-- Eyes -->
          <circle cx="41" cy="50" r="2.5" fill="#3D2B24"/>
          <circle cx="59" cy="50" r="2.5" fill="#3D2B24"/>
          <!-- Smile -->
          <path d="M 44 61 Q 50 69 56 61" fill="#FFFFFF" stroke="#3D2B24" stroke-width="2"/>
        </svg>
      `
    },
    {
      id: 'avatar-river',
      name: 'River',
      tagline: 'Cool & Relaxed',
      bg: '#E0F2F1',
      border: '#80CBC4',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#E0F2F1" stroke="#80CBC4" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#26A69A"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#F5CBA7"/>
          <!-- Head -->
          <ellipse cx="50" cy="52" rx="22" ry="23" fill="#FADBD8"/>
          <!-- Beanie Cap -->
          <path d="M 26 44 C 26 24, 74 24, 74 44 Z" fill="#00695C"/>
          <rect x="25" y="40" width="50" height="9" rx="4" fill="#004D40"/>
          <!-- Eyes -->
          <circle cx="42" cy="53" r="3" fill="#3D2B24"/>
          <circle cx="58" cy="53" r="3" fill="#3D2B24"/>
          <!-- Cheeks -->
          <circle cx="36" cy="58" r="3.5" fill="#4DB6AC" opacity="0.4"/>
          <circle cx="64" cy="58" r="3.5" fill="#4DB6AC" opacity="0.4"/>
          <!-- Smile -->
          <path d="M 44 61 Q 50 68 56 61" fill="none" stroke="#3D2B24" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-echo',
      name: 'Echo',
      tagline: 'Speech & Audio',
      bg: '#EDE7F6',
      border: '#B39DDB',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#EDE7F6" stroke="#B39DDB" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#7E57C2"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#EDBB99"/>
          <!-- Head -->
          <ellipse cx="50" cy="50" rx="22" ry="24" fill="#FDEBD0"/>
          <!-- Hair -->
          <path d="M 28 42 C 28 26, 72 26, 72 42 C 68 28, 32 28, 28 42 Z" fill="#5D4037"/>
          <!-- Headphones Headband -->
          <path d="M 26 48 C 24 22, 76 22, 74 48" fill="none" stroke="#512DA8" stroke-width="4.5"/>
          <!-- Headphone Earcups -->
          <rect x="23" y="44" width="7" height="16" rx="3.5" fill="#311B92"/>
          <rect x="70" y="44" width="7" height="16" rx="3.5" fill="#311B92"/>
          <!-- Eyes -->
          <circle cx="42" cy="50" r="3" fill="#3D2B24"/>
          <circle cx="58" cy="50" r="3" fill="#3D2B24"/>
          <!-- Smile -->
          <path d="M 44 58 Q 50 66 56 58" fill="none" stroke="#3D2B24" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-meadow',
      name: 'Meadow',
      tagline: 'Gentle & Kind',
      bg: '#F1F8E9',
      border: '#C5E1A5',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#F1F8E9" stroke="#C5E1A5" stroke-width="3"/>
          <!-- Hair Bun -->
          <circle cx="50" cy="22" r="9" fill="#6D4C41"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#8BC34A"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#F5CBA7"/>
          <!-- Head -->
          <ellipse cx="50" cy="51" rx="22" ry="24" fill="#FADBD8"/>
          <!-- Hair Front -->
          <path d="M 28 42 C 30 28, 70 28, 72 42 C 60 32, 40 32, 28 42 Z" fill="#6D4C41"/>
          <!-- Eyes -->
          <path d="M 39 50 Q 43 46 47 50" fill="none" stroke="#3D2B24" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M 53 50 Q 57 46 61 50" fill="none" stroke="#3D2B24" stroke-width="2.5" stroke-linecap="round"/>
          <!-- Cheeks -->
          <circle cx="36" cy="56" r="4" fill="#F48FB1" opacity="0.6"/>
          <circle cx="64" cy="56" r="4" fill="#F48FB1" opacity="0.6"/>
          <!-- Smile -->
          <path d="M 44 59 Q 50 66 56 59" fill="none" stroke="#3D2B24" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-harmony',
      name: 'Harmony',
      tagline: 'Joyful & Dynamic',
      bg: '#FFEBEE',
      border: '#EF9A9A',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#FFEBEE" stroke="#EF9A9A" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#E57373"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#EDBB99"/>
          <!-- Head -->
          <ellipse cx="50" cy="51" rx="22" ry="24" fill="#F5CBA7"/>
          <!-- Hair Bandana -->
          <path d="M 28 38 C 28 24, 72 24, 72 38 Z" fill="#C62828"/>
          <rect x="26" y="36" width="48" height="7" rx="3.5" fill="#D32F2F"/>
          <!-- Eyes -->
          <circle cx="42" cy="50" r="3" fill="#3D2B24"/>
          <circle cx="58" cy="50" r="3" fill="#3D2B24"/>
          <!-- Big Smile -->
          <path d="M 42 58 Q 50 70 58 58 Z" fill="#FFFFFF" stroke="#3D2B24" stroke-width="2"/>
        </svg>
      `
    },
    {
      id: 'avatar-nova',
      name: 'Nova',
      tagline: 'Inspiring & Bold',
      bg: '#FFF3E0',
      border: '#FFCC80',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#FFF3E0" stroke="#FFCC80" stroke-width="3"/>
          <!-- Star Accent Top -->
          <path d="M 76 24 L 78 28 L 82 29 L 79 32 L 80 36 L 76 33 L 72 36 L 73 32 L 70 29 L 74 28 Z" fill="#FFB300"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#FB8C00"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#F5CBA7"/>
          <!-- Head -->
          <ellipse cx="50" cy="50" rx="22" ry="24" fill="#FDEBD0"/>
          <!-- Spiky / Dynamic Hair -->
          <path d="M 30 40 L 36 24 L 46 30 L 52 20 L 60 28 L 68 22 L 70 40 Z" fill="#3E2723"/>
          <!-- Eyes -->
          <circle cx="42" cy="50" r="3" fill="#3E2723"/>
          <circle cx="58" cy="50" r="3" fill="#3E2723"/>
          <!-- Smile -->
          <path d="M 44 58 Q 50 66 56 58" fill="none" stroke="#3E2723" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-atlas',
      name: 'Atlas',
      tagline: 'Thoughtful & Steady',
      bg: '#F5EBE6',
      border: '#D7CCC8',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#F5EBE6" stroke="#D7CCC8" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#8D6E63"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#EDBB99"/>
          <!-- Head -->
          <ellipse cx="50" cy="50" rx="22" ry="24" fill="#FADBD8"/>
          <!-- Hair Side Part -->
          <path d="M 28 42 C 28 26, 72 24, 72 40 C 64 30, 40 28, 28 42 Z" fill="#1A252C"/>
          <!-- Eyes -->
          <circle cx="42" cy="51" r="3" fill="#1A252C"/>
          <circle cx="58" cy="51" r="3" fill="#1A252C"/>
          <!-- Eyebrows -->
          <path d="M 38 46 Q 42 44 46 46" fill="none" stroke="#1A252C" stroke-width="2"/>
          <path d="M 54 46 Q 58 44 62 46" fill="none" stroke="#1A252C" stroke-width="2"/>
          <!-- Smile -->
          <path d="M 44 60 Q 50 67 56 60" fill="none" stroke="#1A252C" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-bloom',
      name: 'Bloom',
      tagline: 'Friendly & Radiant',
      bg: '#FCE4EC',
      border: '#F48FB1',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#FCE4EC" stroke="#F48FB1" stroke-width="3"/>
          <!-- Shirt -->
          <path d="M 22 95 Q 50 78 78 95 Z" fill="#EC407A"/>
          <!-- Neck -->
          <rect x="44" y="65" width="12" height="15" rx="4" fill="#F5CBA7"/>
          <!-- Head -->
          <ellipse cx="50" cy="51" rx="22" ry="24" fill="#FDEBD0"/>
          <!-- Hair -->
          <path d="M 28 44 C 30 26, 70 26, 72 44 C 60 30, 38 30, 28 44 Z" fill="#4E342E"/>
          <!-- Flower Clip -->
          <circle cx="68" cy="36" r="4.5" fill="#FFEB3B"/>
          <circle cx="68" cy="36" r="2" fill="#E91E63"/>
          <!-- Eyes -->
          <ellipse cx="42" cy="51" rx="3.5" ry="3" fill="#3E2723"/>
          <ellipse cx="58" cy="51" rx="3.5" ry="3" fill="#3E2723"/>
          <circle cx="43" cy="50" r="1" fill="#FFFFFF"/>
          <circle cx="59" cy="50" r="1" fill="#FFFFFF"/>
          <!-- Cheeks -->
          <circle cx="36" cy="57" r="4" fill="#F06292" opacity="0.6"/>
          <circle cx="64" cy="57" r="4" fill="#F06292" opacity="0.6"/>
          <!-- Smile -->
          <path d="M 44 60 Q 50 67 56 60" fill="none" stroke="#3E2723" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-otter',
      name: 'Otter Pal',
      tagline: 'Fluency Buddy',
      bg: '#FFF3E0',
      border: '#FFE082',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#FFF3E0" stroke="#FFE082" stroke-width="3"/>
          <!-- Otter Ears -->
          <circle cx="28" cy="34" r="8" fill="#795548"/>
          <circle cx="28" cy="34" r="4.5" fill="#D7CCC8"/>
          <circle cx="72" cy="34" r="8" fill="#795548"/>
          <circle cx="72" cy="34" r="4.5" fill="#D7CCC8"/>
          <!-- Otter Body / Shoulders -->
          <path d="M 22 95 Q 50 74 78 95 Z" fill="#8D6E63"/>
          <!-- Otter Head -->
          <ellipse cx="50" cy="50" rx="26" ry="24" fill="#8D6E63"/>
          <!-- Otter Muzzle -->
          <ellipse cx="50" cy="56" rx="14" ry="10" fill="#FFF8E1"/>
          <polygon points="50,50 46,55 54,55" fill="#3E2723"/>
          <!-- Whiskers -->
          <line x1="34" y1="56" x2="26" y2="54" stroke="#5D4037" stroke-width="1.8"/>
          <line x1="34" y1="58" x2="26" y2="60" stroke="#5D4037" stroke-width="1.8"/>
          <line x1="66" y1="56" x2="74" y2="54" stroke="#5D4037" stroke-width="1.8"/>
          <line x1="66" y1="58" x2="74" y2="60" stroke="#5D4037" stroke-width="1.8"/>
          <!-- Eyes -->
          <circle cx="41" cy="44" r="3.5" fill="#2E1C14"/>
          <circle cx="59" cy="44" r="3.5" fill="#2E1C14"/>
          <circle cx="42" cy="43" r="1" fill="#FFFFFF"/>
          <circle cx="60" cy="43" r="1" fill="#FFFFFF"/>
          <!-- Smile -->
          <path d="M 47 58 Q 50 61 53 58" fill="none" stroke="#3E2723" stroke-width="2" stroke-linecap="round"/>
        </svg>
      `
    },
    {
      id: 'avatar-star',
      name: 'Star Speaker',
      tagline: 'Confident & Proud',
      bg: '#FFFDE7',
      border: '#FFF59D',
      render: (size = 64) => `
        <svg viewBox="0 0 100 100" width="${size}" height="${size}" style="border-radius:50%; display:block;" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" fill="#FFFDE7" stroke="#FFF59D" stroke-width="3"/>
          <!-- Big Golden Star Badge -->
          <polygon points="50,18 58,35 77,36 62,49 67,68 50,57 33,68 38,49 23,36 42,35" fill="#FFCA28" stroke="#FFA000" stroke-width="2"/>
          <!-- Friendly Star Face -->
          <circle cx="44" cy="44" r="3" fill="#3D2B24"/>
          <circle cx="56" cy="44" r="3" fill="#3D2B24"/>
          <circle cx="45" cy="43" r="1" fill="#FFFFFF"/>
          <circle cx="57" cy="43" r="1" fill="#FFFFFF"/>
          <circle cx="39" cy="49" r="3" fill="#FF8A65" opacity="0.6"/>
          <circle cx="61" cy="49" r="3" fill="#FF8A65" opacity="0.6"/>
          <!-- Smile -->
          <path d="M 45 50 Q 50 56 55 50" fill="none" stroke="#3D2B24" stroke-width="2.5" stroke-linecap="round"/>
          <!-- Ribbon Base -->
          <path d="M 38 68 L 30 88 L 42 82 L 48 70 Z" fill="#E53935"/>
          <path d="M 62 68 L 70 88 L 58 82 L 52 70 Z" fill="#C62828"/>
        </svg>
      `
    }
  ],

  getAvatar(avatarId) {
    const defaultAvatar = this.avatars[0];
    if (!avatarId) return defaultAvatar;
    const clean = String(avatarId).toLowerCase().trim();
    return this.avatars.find(a => 
      a.id.toLowerCase() === clean || 
      a.name.toLowerCase() === clean ||
      a.id.replace('avatar-', '').toLowerCase() === clean ||
      clean.includes(a.name.toLowerCase()) ||
      clean.includes(a.id.replace('avatar-', '').toLowerCase())
    ) || defaultAvatar;
  },

  render(avatarId, size = 64) {
    const avatar = this.getAvatar(avatarId);
    return avatar.render(size);
  }
};

if (typeof window !== 'undefined') {
  window.AvatarEngine = AvatarEngine;
}
