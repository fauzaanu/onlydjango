/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["../../**/*{.html,.js,forms.py}"], // .py because django forms.py files could contain tailwind classes
    theme: {
        extend: {
            colors: {
                // Light mode (default)
                "background": "#f5f5f5",
                "primary": "#000000",
                "secondary": "#939393",
                "accent": "#7e008a",
                "accent-alt": "#316fcb",
                // purple gold Teal pinkish blue
                "purple": "#7e008a",
                "gold": "#d2a679",
                "teal": "#3dc5f9",
                "pinkish-blue": "#641dcc",
            },
            fontFamily: {
                'body': ['ak-rasmee'],
                'heading': ['aamu-fk'],
                'afk': ['aamu-fk'],
                'rasmee': ['ak-rasmee'],
                'type-bold': ['mv-type-bold'],
                'waheed': ['mv_waheed'],
                'waheed-smooth': ['mv-waheed-smooth'],
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
            },
            boxShadow: {
                'left': '50px 0 10px -50px rgba(255,255,255,0.5)',
                'right': '-50px 0 10px -50px rgba(255,255,255,0.5)',
                'modern': '0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.06)',
            },
        },

    },
}



