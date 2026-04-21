/** @type {import('tailwindcss').Config} */
export default {
  theme: {
    extend: {
    colors: {
        primary: {
            '50': 'hsl(NaN, NaN%, 97%)',
            '100': 'hsl(NaN, NaN%, 94%)',
            '200': 'hsl(NaN, NaN%, 86%)',
            '300': 'hsl(NaN, NaN%, 76%)',
            '400': 'hsl(NaN, NaN%, 64%)',
            '500': 'hsl(NaN, NaN%, 50%)',
            '600': 'hsl(NaN, NaN%, 40%)',
            '700': 'hsl(NaN, NaN%, 32%)',
            '800': 'hsl(NaN, NaN%, 24%)',
            '900': 'hsl(NaN, NaN%, 16%)',
            '950': 'hsl(NaN, NaN%, 10%)',
            DEFAULT: '#00d9ff'
        },
        secondary: {
            '50': 'hsl(NaN, NaN%, 97%)',
            '100': 'hsl(NaN, NaN%, 94%)',
            '200': 'hsl(NaN, NaN%, 86%)',
            '300': 'hsl(NaN, NaN%, 76%)',
            '400': 'hsl(NaN, NaN%, 64%)',
            '500': 'hsl(NaN, NaN%, 50%)',
            '600': 'hsl(NaN, NaN%, 40%)',
            '700': 'hsl(NaN, NaN%, 32%)',
            '800': 'hsl(NaN, NaN%, 24%)',
            '900': 'hsl(NaN, NaN%, 16%)',
            '950': 'hsl(NaN, NaN%, 10%)',
            DEFAULT: '#e8e8f0'
        },
        accent: {
            '50': 'hsl(NaN, NaN%, 97%)',
            '100': 'hsl(NaN, NaN%, 94%)',
            '200': 'hsl(NaN, NaN%, 86%)',
            '300': 'hsl(NaN, NaN%, 76%)',
            '400': 'hsl(NaN, NaN%, 64%)',
            '500': 'hsl(NaN, NaN%, 50%)',
            '600': 'hsl(NaN, NaN%, 40%)',
            '700': 'hsl(NaN, NaN%, 32%)',
            '800': 'hsl(NaN, NaN%, 24%)',
            '900': 'hsl(NaN, NaN%, 16%)',
            '950': 'hsl(NaN, NaN%, 10%)',
            DEFAULT: '#00b1ff'
        },
        'neutral-50': '#000000',
        'neutral-100': '#ffffff',
        background: '#0a0a0f',
        foreground: '#000000'
    },
    fontFamily: {
        body: [
            'ui-sans-serif',
            'sans-serif'
        ],
        font2: [
            'Cinzel',
            'sans-serif'
        ]
    },
    fontSize: {
        '12': [
            '12px',
            {
                lineHeight: '16px',
                letterSpacing: '0.72px'
            }
        ],
        '14': [
            '14px',
            {
                lineHeight: '20px',
                letterSpacing: '1.152px'
            }
        ],
        '16': [
            '16px',
            {
                lineHeight: '24px'
            }
        ],
        '20': [
            '20px',
            {
                lineHeight: '28px'
            }
        ],
        '28': [
            '28px',
            {
                lineHeight: '39.2px',
                letterSpacing: '0.42px'
            }
        ],
        '14.4': [
            '14.4px',
            {
                lineHeight: '21.6px',
                letterSpacing: '1.152px'
            }
        ],
        '11.2': [
            '11.2px',
            {
                lineHeight: '16.8px',
                letterSpacing: '0.56px'
            }
        ]
    },
    spacing: {
        '0': '4px',
        '1': '112px'
    },
    borderRadius: {
        md: '6px',
        lg: '16px'
    },
    boxShadow: {
        sm: 'rgb(0, 217, 255) 0px 0px 7.8234px 0px',
        md: 'rgb(74, 144, 226) 0px 0px 8.9496px 0px'
    },
    screens: {
        md: '768px',
        lg: '1024px'
    },
    transitionDuration: {
        '150': '0.15s',
        '300': '0.3s',
        '500': '0.5s',
        '700': '0.7s'
    },
    transitionTimingFunction: {
        custom: 'cubic-bezier(0, 0, 0.2, 1)'
    },
    container: {
        center: true,
        padding: '32px'
    },
    maxWidth: {
        container: '1440px'
    }
},
  },
};
