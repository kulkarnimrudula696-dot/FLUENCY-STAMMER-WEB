/**
 * FLUENCY Mascot SVG Illustration & State Animation Engine
 * Supports 8 friendly companions:
 * 1. 🦦 Otter (Sammy) - Friendly Practice Buddy (Default)
 * 2. 🐨 Koala (Koby) - Calm & Comforting
 * 3. 🦫 Capybara (Cappy) - Chill & Zero-Pressure
 * 4. 🦊 Red Panda (Pip) - Cute & Unique
 * 5. 🐹 Hamster (Boba) - Energetic & Encouraging
 * 6. 🦆 Duck (Ducky) - Playful & Cheerful
 * 7. 🦭 Seal (Snooze) - Soft & Lovable
 * 8. 🩷 Axolotl (Lottie) - Unique & Gen-Z
 *
 * States supported: 'waving', 'smiling', 'listening', 'holding_mic', 'breathing', 'celebrating'
 */

const MascotEngine = {
  _svgCache: {},
  /**
   * Render mascot SVG markup (Memoized for optimal performance)
   * @param {string} mascotId - otter, koala, capybara, red_panda, hamster, duck, seal, axolotl
   * @param {string} state - waving, smiling, listening, holding_mic, breathing, celebrating
   * @param {number} size - width/height in px
   */
  render(mascotId = 'otter', state = 'smiling', size = 120) {
    const key = `${mascotId}_${state}_${size}`;
    if (this._svgCache[key]) {
      return this._svgCache[key];
    }
    const fn = this.renderers[mascotId] || this.renderers.otter;
    const svg = fn.call(this, state, size);
    this._svgCache[key] = svg;
    return svg;
  },

  renderers: {
    // 1. OTTER (Sammy) — Default
    otter(state, size) {
      const isBreathing = state === 'breathing';
      const isListening = state === 'listening';
      const isWaving = state === 'waving';
      const isCelebrating = state === 'celebrating';

      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${isBreathing ? 'anim-breathe' : ''}">
          <!-- Background Glow / Circle -->
          <circle cx="70" cy="70" r="62" fill="#FFF4DE" stroke="#E8D9CE" stroke-width="2.5"/>
          
          <!-- Outer Listening Waves if state is listening -->
          ${isListening ? `
            <circle cx="28" cy="70" r="14" fill="none" stroke="#9A633F" stroke-width="2.5" class="anim-listen-wave" stroke-dasharray="4 2"/>
            <circle cx="112" cy="70" r="14" fill="none" stroke="#9A633F" stroke-width="2.5" class="anim-listen-wave" stroke-dasharray="4 2"/>
          ` : ''}

          <!-- Otter Ears -->
          <circle cx="38" cy="46" r="12" fill="#845030" stroke="#3D2B24" stroke-width="2"/>
          <circle cx="38" cy="46" r="6" fill="#F4ECE6"/>
          <circle cx="102" cy="46" r="12" fill="#845030" stroke="#3D2B24" stroke-width="2"/>
          <circle cx="102" cy="46" r="6" fill="#F4ECE6"/>

          <!-- Otter Head & Body Base -->
          <ellipse cx="70" cy="98" rx="38" ry="32" fill="#9A633F" stroke="#3D2B24" stroke-width="2.5"/>
          <!-- Belly Cream Patch -->
          <ellipse cx="70" cy="104" rx="24" ry="22" fill="#FFF9EE"/>

          <ellipse cx="70" cy="62" rx="36" ry="32" fill="#9A633F" stroke="#3D2B24" stroke-width="2.5"/>
          <!-- Cheeks Muzzle -->
          <ellipse cx="70" cy="72" rx="22" ry="16" fill="#FFF9EE" stroke="#3D2B24" stroke-width="1.5"/>

          <!-- Eyes -->
          <circle cx="56" cy="58" r="4.5" fill="#3D2B24" class="anim-blink"/>
          <circle cx="58" cy="56" r="1.5" fill="#FFFFFF"/>
          <circle cx="84" cy="58" r="4.5" fill="#3D2B24" class="anim-blink"/>
          <circle cx="86" cy="56" r="1.5" fill="#FFFFFF"/>

          <!-- Blushing Cheeks -->
          <circle cx="46" cy="68" r="5" fill="#FFAAA6" opacity="0.6"/>
          <circle cx="94" cy="68" r="5" fill="#FFAAA6" opacity="0.6"/>

          <!-- Nose -->
          <polygon points="70,66 64,72 76,72" fill="#3D2B24"/>
          <!-- Smile -->
          <path d="M 64,74 Q 70,82 76,74" fill="none" stroke="#3D2B24" stroke-width="2" stroke-linecap="round"/>

          <!-- Whiskers -->
          <line x1="42" y1="70" x2="30" y2="67" stroke="#3D2B24" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="42" y1="74" x2="28" y2="76" stroke="#3D2B24" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="98" y1="70" x2="110" y2="67" stroke="#3D2B24" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="98" y1="74" x2="112" y2="76" stroke="#3D2B24" stroke-width="1.5" stroke-linecap="round"/>

          <!-- Paws -->
          ${isWaving ? `
            <!-- Left Waving Paw -->
            <g class="anim-wave-arm">
              <ellipse cx="32" cy="70" rx="9" ry="12" fill="#9A633F" stroke="#3D2B24" stroke-width="2"/>
            </g>
            <!-- Right Paw on belly -->
            <ellipse cx="94" cy="98" rx="8" ry="10" fill="#9A633F" stroke="#3D2B24" stroke-width="2"/>
          ` : isCelebrating ? `
            <!-- Both Paws Up in Celebration -->
            <ellipse cx="34" cy="62" rx="9" ry="13" fill="#9A633F" stroke="#3D2B24" stroke-width="2"/>
            <ellipse cx="106" cy="62" rx="9" ry="13" fill="#9A633F" stroke="#3D2B24" stroke-width="2"/>
            <!-- Confetti sparkles -->
            <circle cx="30" cy="30" r="3" fill="#FFC83D"/>
            <circle cx="110" cy="32" r="3" fill="#FF8A65"/>
            <circle cx="70" cy="20" r="2.5" fill="#4DB6AC"/>
          ` : `
            <!-- Standard Resting / Mic Paws -->
            <ellipse cx="48" cy="96" rx="9" ry="11" fill="#9A633F" stroke="#3D2B24" stroke-width="2"/>
            <ellipse cx="92" cy="96" rx="9" ry="11" fill="#9A633F" stroke="#3D2B24" stroke-width="2"/>
          `}

          ${state === 'holding_mic' ? `
            <!-- Microphone In Paw -->
            <rect x="86" y="80" width="8" height="18" rx="3" fill="#3D2B24"/>
            <circle cx="90" cy="78" r="6" fill="#8E9AA0" stroke="#3D2B24" stroke-width="1.5"/>
          ` : ''}
        </svg>
      `;
    },

    // 2. KOALA (Koby)
    koala(state, size) {
      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${state === 'breathing' ? 'anim-breathe' : ''}">
          <circle cx="70" cy="70" r="62" fill="#EDF2F7" stroke="#CBD5E1" stroke-width="2.5"/>
          
          <!-- Fluffy Koala Ears -->
          <circle cx="34" cy="48" r="18" fill="#94A3B8" stroke="#334155" stroke-width="2"/>
          <circle cx="34" cy="48" r="10" fill="#FFFFFF"/>
          <circle cx="106" cy="48" r="18" fill="#94A3B8" stroke="#334155" stroke-width="2"/>
          <circle cx="106" cy="48" r="10" fill="#FFFFFF"/>

          <!-- Body -->
          <ellipse cx="70" cy="100" rx="38" ry="30" fill="#94A3B8" stroke="#334155" stroke-width="2.5"/>
          <ellipse cx="70" cy="104" rx="22" ry="20" fill="#FFFFFF"/>

          <!-- Head -->
          <ellipse cx="70" cy="65" rx="36" ry="30" fill="#94A3B8" stroke="#334155" stroke-width="2.5"/>

          <!-- Eyes -->
          <circle cx="54" cy="60" r="4.5" fill="#334155" class="anim-blink"/>
          <circle cx="56" cy="58" r="1.5" fill="#FFFFFF"/>
          <circle cx="86" cy="60" r="4.5" fill="#334155" class="anim-blink"/>
          <circle cx="88" cy="58" r="1.5" fill="#FFFFFF"/>

          <!-- Large Koala Nose -->
          <ellipse cx="70" cy="72" rx="11" ry="16" fill="#334155"/>
          <ellipse cx="68" cy="68" rx="3" ry="5" fill="#64748B" opacity="0.6"/>

          <!-- Cheeks -->
          <circle cx="44" cy="70" r="5" fill="#FFAAA6" opacity="0.5"/>
          <circle cx="96" cy="70" r="5" fill="#FFAAA6" opacity="0.5"/>

          <!-- Paws -->
          <ellipse cx="48" cy="98" rx="8" ry="10" fill="#94A3B8" stroke="#334155" stroke-width="2"/>
          <ellipse cx="92" cy="98" rx="8" ry="10" fill="#94A3B8" stroke="#334155" stroke-width="2"/>
        </svg>
      `;
    },

    // 3. CAPYBARA (Cappy)
    capybara(state, size) {
      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${state === 'breathing' ? 'anim-breathe' : ''}">
          <circle cx="70" cy="70" r="62" fill="#F7EFE5" stroke="#E2D4C3" stroke-width="2.5"/>
          
          <!-- Capybara Small Ears -->
          <circle cx="40" cy="45" r="9" fill="#8C6239" stroke="#3D2B24" stroke-width="2"/>
          <circle cx="100" cy="45" r="9" fill="#8C6239" stroke="#3D2B24" stroke-width="2"/>

          <!-- Body -->
          <ellipse cx="70" cy="100" rx="39" ry="30" fill="#A47547" stroke="#3D2B24" stroke-width="2.5"/>

          <!-- Signature Blocky Head -->
          <rect x="36" y="44" width="68" height="52" rx="22" fill="#A47547" stroke="#3D2B24" stroke-width="2.5"/>

          <!-- Calm Zen Slit Eyes -->
          <line x1="48" y1="64" x2="58" y2="64" stroke="#3D2B24" stroke-width="3" stroke-linecap="round"/>
          <line x1="82" y1="64" x2="92" y2="64" stroke="#3D2B24" stroke-width="3" stroke-linecap="round"/>

          <!-- Capybara Snout -->
          <ellipse cx="70" cy="80" rx="16" ry="12" fill="#8C6239" stroke="#3D2B24" stroke-width="2"/>
          <!-- Nostrils & Mouth -->
          <circle cx="65" cy="78" r="2.5" fill="#3D2B24"/>
          <circle cx="75" cy="78" r="2.5" fill="#3D2B24"/>
          <line x1="70" y1="82" x2="70" y2="87" stroke="#3D2B24" stroke-width="2"/>

          <!-- Paws -->
          <ellipse cx="50" cy="104" rx="8" ry="8" fill="#8C6239" stroke="#3D2B24" stroke-width="2"/>
          <ellipse cx="90" cy="104" rx="8" ry="8" fill="#8C6239" stroke="#3D2B24" stroke-width="2"/>

          <!-- Little Orange / Leaf on Head for extra charm -->
          <circle cx="70" cy="38" r="7" fill="#FFA726" stroke="#3D2B24" stroke-width="1.5"/>
          <path d="M 70,31 Q 74,27 75,30" fill="none" stroke="#2E7D32" stroke-width="2"/>
        </svg>
      `;
    },

    // 4. RED PANDA (Pip)
    red_panda(state, size) {
      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${state === 'breathing' ? 'anim-breathe' : ''}">
          <circle cx="70" cy="70" r="62" fill="#FDEEE8" stroke="#F6CCC0" stroke-width="2.5"/>
          
          <!-- Triangular Fluffy Ears -->
          <polygon points="32,56 46,30 58,54" fill="#C85A32" stroke="#3D2B24" stroke-width="2"/>
          <polygon points="36,52 46,36 54,52" fill="#FFFFFF"/>
          <polygon points="108,56 94,30 82,54" fill="#C85A32" stroke="#3D2B24" stroke-width="2"/>
          <polygon points="104,52 94,36 86,52" fill="#FFFFFF"/>

          <!-- Body -->
          <ellipse cx="70" cy="100" rx="36" ry="28" fill="#422216" stroke="#3D2B24" stroke-width="2.5"/>
          <!-- Head -->
          <ellipse cx="70" cy="65" rx="36" ry="30" fill="#C85A32" stroke="#3D2B24" stroke-width="2.5"/>

          <!-- White Facial Markings -->
          <ellipse cx="44" cy="62" rx="10" ry="12" fill="#FFFFFF"/>
          <ellipse cx="96" cy="62" rx="10" ry="12" fill="#FFFFFF"/>
          <ellipse cx="70" cy="74" rx="16" ry="12" fill="#FFFFFF"/>

          <!-- Eyes -->
          <circle cx="54" cy="62" r="4.5" fill="#3D2B24" class="anim-blink"/>
          <circle cx="86" cy="62" r="4.5" fill="#3D2B24" class="anim-blink"/>

          <!-- Nose & Smile -->
          <ellipse cx="70" cy="71" rx="4" ry="3" fill="#3D2B24"/>
          <path d="M 66,75 Q 70,80 74,75" fill="none" stroke="#3D2B24" stroke-width="2" stroke-linecap="round"/>

          <!-- Red Panda Cheek Stripes -->
          <path d="M 52,68 L 46,80" stroke="#C85A32" stroke-width="3" stroke-linecap="round"/>
          <path d="M 88,68 L 94,80" stroke="#C85A32" stroke-width="3" stroke-linecap="round"/>
        </svg>
      `;
    },

    // 5. HAMSTER (Boba)
    hamster(state, size) {
      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${state === 'breathing' ? 'anim-breathe' : ''}">
          <circle cx="70" cy="70" r="62" fill="#FFF3E0" stroke="#FFE0B2" stroke-width="2.5"/>
          
          <!-- Round Hamster Ears -->
          <circle cx="42" cy="46" r="12" fill="#E67E22" stroke="#3D2B24" stroke-width="2"/>
          <circle cx="42" cy="46" r="6" fill="#F8BBD0"/>
          <circle cx="98" cy="46" r="12" fill="#E67E22" stroke="#3D2B24" stroke-width="2"/>
          <circle cx="98" cy="46" r="6" fill="#F8BBD0"/>

          <!-- Big Chubby Round Body & Cheeks -->
          <ellipse cx="70" cy="76" rx="40" ry="36" fill="#F39C12" stroke="#3D2B24" stroke-width="2.5"/>
          <ellipse cx="70" cy="84" rx="28" ry="24" fill="#FFFFFF"/>

          <!-- Big Sparkling Eyes -->
          <circle cx="52" cy="64" r="6" fill="#3D2B24" class="anim-blink"/>
          <circle cx="54" cy="62" r="2" fill="#FFFFFF"/>
          <circle cx="88" cy="64" r="6" fill="#3D2B24" class="anim-blink"/>
          <circle cx="90" cy="62" r="2" fill="#FFFFFF"/>

          <!-- Rosy Chubby Cheeks -->
          <circle cx="40" cy="74" r="7" fill="#FF8A80" opacity="0.7"/>
          <circle cx="100" cy="74" r="7" fill="#FF8A80" opacity="0.7"/>

          <!-- Tiny Hamster Nose & Mouth -->
          <polygon points="70,72 67,76 73,76" fill="#E74C3C"/>
          <path d="M 66,78 Q 70,83 74,78" fill="none" stroke="#3D2B24" stroke-width="2" stroke-linecap="round"/>
        </svg>
      `;
    },

    // 6. DUCK (Ducky)
    duck(state, size) {
      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${state === 'breathing' ? 'anim-breathe' : ''}">
          <circle cx="70" cy="70" r="62" fill="#E8F5E9" stroke="#C8E6C9" stroke-width="2.5"/>
          
          <!-- Round Duck Body -->
          <ellipse cx="70" cy="94" rx="36" ry="26" fill="#FFF176" stroke="#3D2B24" stroke-width="2.5"/>
          <!-- Head -->
          <circle cx="70" cy="60" r="28" fill="#FFF176" stroke="#3D2B24" stroke-width="2.5"/>

          <!-- Eyes -->
          <circle cx="56" cy="56" r="4.5" fill="#3D2B24" class="anim-blink"/>
          <circle cx="58" cy="54" r="1.5" fill="#FFFFFF"/>
          <circle cx="84" cy="56" r="4.5" fill="#3D2B24" class="anim-blink"/>
          <circle cx="86" cy="54" r="1.5" fill="#FFFFFF"/>

          <!-- Cheeks -->
          <circle cx="46" cy="66" r="5" fill="#FFAAA6" opacity="0.6"/>
          <circle cx="94" cy="66" r="5" fill="#FFAAA6" opacity="0.6"/>

          <!-- Wide Friendly Bill -->
          <ellipse cx="70" cy="68" rx="16" ry="9" fill="#FF9800" stroke="#3D2B24" stroke-width="2"/>
          <line x1="62" y1="68" x2="78" y2="68" stroke="#E65100" stroke-width="1.5"/>

          <!-- Wings -->
          <ellipse cx="40" cy="92" rx="8" ry="12" fill="#FFEE58" stroke="#3D2B24" stroke-width="2" transform="rotate(-15 40 92)"/>
          <ellipse cx="100" cy="92" rx="8" ry="12" fill="#FFEE58" stroke="#3D2B24" stroke-width="2" transform="rotate(15 100 92)"/>
        </svg>
      `;
    },

    // 7. SEAL (Snooze)
    seal(state, size) {
      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${state === 'breathing' ? 'anim-breathe' : ''}">
          <circle cx="70" cy="70" r="62" fill="#ECEFF1" stroke="#CFD8DC" stroke-width="2.5"/>
          
          <!-- Round Soft Seal Body -->
          <ellipse cx="70" cy="80" rx="38" ry="34" fill="#B0BEC5" stroke="#37474F" stroke-width="2.5"/>
          <ellipse cx="70" cy="90" rx="24" ry="20" fill="#ECEFF1"/>

          <!-- Eyes -->
          <circle cx="54" cy="66" r="5" fill="#263238" class="anim-blink"/>
          <circle cx="56" cy="64" r="1.5" fill="#FFFFFF"/>
          <circle cx="86" cy="66" r="5" fill="#263238" class="anim-blink"/>
          <circle cx="88" cy="64" r="1.5" fill="#FFFFFF"/>

          <!-- Muzzle & Cute Nose -->
          <ellipse cx="70" cy="78" rx="16" ry="12" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5"/>
          <polygon points="70,72 65,77 75,77" fill="#263238"/>
          <path d="M 64,80 Q 70,86 76,80" fill="none" stroke="#263238" stroke-width="2" stroke-linecap="round"/>

          <!-- Whiskers -->
          <circle cx="62" cy="78" r="1" fill="#263238"/>
          <circle cx="60" cy="81" r="1" fill="#263238"/>
          <circle cx="78" cy="78" r="1" fill="#263238"/>
          <circle cx="80" cy="81" r="1" fill="#263238"/>

          <!-- Flippers -->
          <ellipse cx="38" cy="95" rx="8" ry="14" fill="#90A4AE" stroke="#37474F" stroke-width="2" transform="rotate(30 38 95)"/>
          <ellipse cx="102" cy="95" rx="8" ry="14" fill="#90A4AE" stroke="#37474F" stroke-width="2" transform="rotate(-30 102 95)"/>
        </svg>
      `;
    },

    // 8. AXOLOTL (Lottie)
    axolotl(state, size) {
      return `
        <svg viewBox="0 0 140 140" width="${size}" height="${size}" class="mascot-svg ${state === 'breathing' ? 'anim-breathe' : ''}">
          <circle cx="70" cy="70" r="62" fill="#FCE4EC" stroke="#F8BBD0" stroke-width="2.5"/>
          
          <!-- Pink Frilly Gills -->
          <path d="M 36,50 Q 20,40 26,30 Q 34,42 40,54" fill="#EC407A" stroke="#AD1457" stroke-width="1.5"/>
          <path d="M 32,62 Q 14,60 20,50 Q 30,60 36,66" fill="#EC407A" stroke="#AD1457" stroke-width="1.5"/>
          <path d="M 36,74 Q 22,78 28,86 Q 34,78 40,74" fill="#EC407A" stroke="#AD1457" stroke-width="1.5"/>

          <path d="M 104,50 Q 120,40 114,30 Q 106,42 100,54" fill="#EC407A" stroke="#AD1457" stroke-width="1.5"/>
          <path d="M 108,62 Q 126,60 120,50 Q 110,60 104,66" fill="#EC407A" stroke="#AD1457" stroke-width="1.5"/>
          <path d="M 104,74 Q 118,78 112,86 Q 106,78 100,74" fill="#EC407A" stroke="#AD1457" stroke-width="1.5"/>

          <!-- Axolotl Head & Body -->
          <ellipse cx="70" cy="94" rx="32" ry="24" fill="#F48FB1" stroke="#AD1457" stroke-width="2.5"/>
          <ellipse cx="70" cy="65" rx="34" ry="26" fill="#F8BBD0" stroke="#AD1457" stroke-width="2.5"/>

          <!-- Eyes -->
          <circle cx="52" cy="62" r="5" fill="#3D2B24" class="anim-blink"/>
          <circle cx="54" cy="60" r="1.5" fill="#FFFFFF"/>
          <circle cx="88" cy="62" r="5" fill="#3D2B24" class="anim-blink"/>
          <circle cx="90" cy="60" r="1.5" fill="#FFFFFF"/>

          <!-- Big Axolotl Derp Smile -->
          <path d="M 58,72 Q 70,82 82,72" fill="none" stroke="#AD1457" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="46" cy="68" r="4.5" fill="#EC407A" opacity="0.6"/>
          <circle cx="94" cy="68" r="4.5" fill="#EC407A" opacity="0.6"/>
        </svg>
      `;
    }
  }
};
