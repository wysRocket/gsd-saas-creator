"""
scaffold.py — Generates a Next.js 14 + Firebase + shadcn/ui project skeleton.

Usage:
    python scripts/scaffold.py [output_dir]

    # With design token injection from a designlang output:
    DESIGN_TOKENS=./path/to/design-tokens.json python scripts/scaffold.py [output_dir]

Output defaults to ./output/<project_name>/

Environment variables:
    PROJECT_NAME      — kebab-case name of the project
    DESIGN_TOKENS     — path to designlang design-tokens.json (optional)
    PRIMARY_COLOR     — hex color (default: #6366f1, overridden by DESIGN_TOKENS)
    FONT_SANS         — font family name (default: Inter)
"""

import os
import sys
import json
import re
import textwrap
from pathlib import Path


def load_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


PROJECT_NAME = load_env("PROJECT_NAME", "my-saas-app")
OUTPUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output") / PROJECT_NAME.lower().replace(" ", "-")

# ---------------------------------------------------------------------------
# Design token loading (from designlang output)
# ---------------------------------------------------------------------------

def _load_design_tokens() -> dict:
    """Load design tokens from DESIGN_TOKENS env path or look in common locations."""
    token_path = os.environ.get("DESIGN_TOKENS", "")
    candidates = []
    if token_path:
        candidates.append(Path(token_path))
    # Auto-discover in output dir or cwd
    candidates += [
        OUTPUT_DIR / "design" / "design-tokens.json",
        OUTPUT_DIR / "design-tokens.json",
        Path("design-tokens.json"),
    ]
    for p in candidates:
        if p.exists():
            try:
                data = json.loads(p.read_text())
                print(f"  [tokens] loaded from {p}")
                return data
            except Exception:
                pass
    return {}


def _extract_colors(tokens: dict) -> dict:
    """Extract primary/secondary/bg/text from designlang tokens.json."""
    defaults = {
        "primary": os.environ.get("PRIMARY_COLOR", "#6366f1"),
        "secondary": "#8b5cf6",
        "background": "#ffffff",
        "foreground": "#0f172a",
        "muted": "#f1f5f9",
        "border": "#e2e8f0",
    }
    if not tokens:
        return defaults

    # designlang tokens.json structure varies — try multiple paths
    colors = tokens.get("colors", tokens.get("theme", {}).get("colors", {}))
    if isinstance(colors, dict):
        # Flat hex map (e.g. {"primary": "#00d9ff", "background": "#0a0a0f"})
        mapping = {
            "primary": colors.get("primary", colors.get("brand", defaults["primary"])),
            "secondary": colors.get("secondary", colors.get("accent", defaults["secondary"])),
            "background": colors.get("background", colors.get("bg", defaults["background"])),
            "foreground": colors.get("foreground", colors.get("text", defaults["foreground"])),
            "muted": colors.get("muted", colors.get("surface", defaults["muted"])),
            "border": colors.get("border", colors.get("outline", defaults["border"])),
        }
        return {k: v if isinstance(v, str) else defaults[k] for k, v in mapping.items()}
    return defaults


def _extract_fonts(tokens: dict) -> dict:
    defaults = {
        "sans": os.environ.get("FONT_SANS", "Inter"),
        "heading": "Inter",
    }
    if not tokens:
        return defaults
    typography = tokens.get("typography", tokens.get("fonts", {}))
    if isinstance(typography, dict):
        body = typography.get("body", typography.get("sans", typography.get("fontFamily", "")))
        heading = typography.get("heading", typography.get("display", body))
        if body:
            defaults["sans"] = body.split(",")[0].strip().strip('"\'')
        if heading:
            defaults["heading"] = heading.split(",")[0].strip().strip('"\'')
    return defaults


# ---------------------------------------------------------------------------
# File content generators (populated after token loading)
# ---------------------------------------------------------------------------

_TOKENS = _load_design_tokens()
_COLORS = _extract_colors(_TOKENS)
_FONTS  = _extract_fonts(_TOKENS)


def package_json() -> str:
    return json.dumps({
        "name": PROJECT_NAME.lower().replace(" ", "-"),
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "test": "jest --passWithNoTests",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "^14.2.0",
            "react": "^18.3.0",
            "react-dom": "^18.3.0",
            "firebase": "^10.12.0",
            "tailwindcss": "^3.4.0",
            "tailwindcss-animate": "^1.0.7",
            "@tailwindcss/forms": "^0.5.0",
            "class-variance-authority": "^0.7.0",
            "clsx": "^2.1.0",
            "lucide-react": "^0.400.0",
            "tailwind-merge": "^2.3.0",
            "@radix-ui/react-slot": "^1.1.0",
            "@radix-ui/react-dialog": "^1.1.0",
            "@radix-ui/react-dropdown-menu": "^2.1.0",
            "@radix-ui/react-toast": "^1.2.0"
        },
        "devDependencies": {
            "@types/node": "^20.0.0",
            "@types/react": "^18.0.0",
            "jest": "^29.0.0",
            "@testing-library/react": "^14.0.0",
            "@testing-library/jest-dom": "^6.0.0",
            "typescript": "^5.0.0",
            "autoprefixer": "^10.4.0",
            "postcss": "^8.4.0"
        }
    }, indent=2)


def tailwind_config() -> str:
    primary = _COLORS["primary"]
    secondary = _COLORS["secondary"]
    background = _COLORS["background"]
    foreground = _COLORS["foreground"]
    muted = _COLORS["muted"]
    border = _COLORS["border"]
    font_sans = _FONTS["sans"]
    font_heading = _FONTS["heading"]

    return textwrap.dedent(f"""\
        /** @type {{import('tailwindcss').Config}} */
        module.exports = {{
          darkMode: ["class"],
          content: [
            "./src/**/*.{{js,ts,jsx,tsx,mdx}}",
            "./app/**/*.{{js,ts,jsx,tsx,mdx}}",
          ],
          theme: {{
            container: {{
              center: true,
              padding: "2rem",
              screens: {{ "2xl": "1400px" }},
            }},
            extend: {{
              colors: {{
                border: "{border}",
                background: "{background}",
                foreground: "{foreground}",
                muted: {{
                  DEFAULT: "{muted}",
                  foreground: "{foreground}",
                }},
                primary: {{
                  DEFAULT: "{primary}",
                  foreground: "#ffffff",
                }},
                secondary: {{
                  DEFAULT: "{secondary}",
                  foreground: "#ffffff",
                }},
              }},
              fontFamily: {{
                sans: ["{font_sans}", "system-ui", "sans-serif"],
                heading: ["{font_heading}", "{font_sans}", "sans-serif"],
              }},
              borderRadius: {{
                lg: "0.5rem",
                md: "calc(0.5rem - 2px)",
                sm: "calc(0.5rem - 4px)",
              }},
              keyframes: {{
                "accordion-down": {{
                  from: {{ height: "0" }},
                  to: {{ height: "var(--radix-accordion-content-height)" }},
                }},
                "accordion-up": {{
                  from: {{ height: "var(--radix-accordion-content-height)" }},
                  to: {{ height: "0" }},
                }},
              }},
              animation: {{
                "accordion-down": "accordion-down 0.2s ease-out",
                "accordion-up": "accordion-up 0.2s ease-out",
              }},
            }},
          }},
          plugins: [require("tailwindcss-animate"), require("@tailwindcss/forms")],
        }};
    """)


def next_config() -> str:
    return textwrap.dedent("""\
        /** @type {import('next').NextConfig} */
        const nextConfig = {
          reactStrictMode: true,
        };

        module.exports = nextConfig;
    """)


def firebase_config_ts() -> str:
    return textwrap.dedent("""\
        import { initializeApp, getApps } from "firebase/app";
        import { getAuth } from "firebase/auth";
        import { getFirestore } from "firebase/firestore";

        const firebaseConfig = {
          apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
          authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
          projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
          storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
          messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
          appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
        };

        const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

        export const auth = getAuth(app);
        export const db = getFirestore(app);
        export default app;
    """)


def cn_util_ts() -> str:
    return textwrap.dedent("""\
        import { type ClassValue, clsx } from "clsx";
        import { twMerge } from "tailwind-merge";

        export function cn(...inputs: ClassValue[]) {
          return twMerge(clsx(inputs));
        }
    """)


def button_component_tsx() -> str:
    return textwrap.dedent("""\
        import * as React from "react";
        import { Slot } from "@radix-ui/react-slot";
        import { cva, type VariantProps } from "class-variance-authority";
        import { cn } from "@/lib/utils";

        const buttonVariants = cva(
          "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
          {
            variants: {
              variant: {
                default: "bg-primary text-primary-foreground hover:bg-primary/90",
                destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
                outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
                secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
                ghost: "hover:bg-accent hover:text-accent-foreground",
                link: "text-primary underline-offset-4 hover:underline",
              },
              size: {
                default: "h-10 px-4 py-2",
                sm: "h-9 rounded-md px-3",
                lg: "h-11 rounded-md px-8",
                icon: "h-10 w-10",
              },
            },
            defaultVariants: {
              variant: "default",
              size: "default",
            },
          }
        );

        export interface ButtonProps
          extends React.ButtonHTMLAttributes<HTMLButtonElement>,
            VariantProps<typeof buttonVariants> {
          asChild?: boolean;
        }

        const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
          ({ className, variant, size, asChild = false, ...props }, ref) => {
            const Comp = asChild ? Slot : "button";
            return (
              <Comp
                className={cn(buttonVariants({ variant, size, className }))}
                ref={ref}
                {...props}
              />
            );
          }
        );
        Button.displayName = "Button";

        export { Button, buttonVariants };
    """)


def index_page_tsx() -> str:
    primary = _COLORS["primary"]
    return textwrap.dedent(f"""\
        import type {{ NextPage }} from "next";
        import Head from "next/head";
        import {{ Button }} from "@/components/ui/button";

        const Home: NextPage = () => {{
          return (
            <>
              <Head>
                <title>{PROJECT_NAME}</title>
              </Head>
              <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-background text-foreground">
                <h1 className="font-heading text-5xl font-bold mb-4">{PROJECT_NAME}</h1>
                <p className="text-muted mb-8 text-lg">Your SaaS is ready. Start building.</p>
                <Button size="lg">Get Started</Button>
              </main>
            </>
          );
        }};

        export default Home;
    """)


def global_css() -> str:
    primary = _COLORS["primary"]
    secondary = _COLORS["secondary"]
    background = _COLORS["background"]
    foreground = _COLORS["foreground"]
    muted = _COLORS["muted"]
    border = _COLORS["border"]
    return textwrap.dedent(f"""\
        @tailwind base;
        @tailwind components;
        @tailwind utilities;

        @layer base {{
          :root {{
            --background: {background};
            --foreground: {foreground};
            --primary: {primary};
            --primary-foreground: #ffffff;
            --secondary: {secondary};
            --secondary-foreground: #ffffff;
            --muted: {muted};
            --muted-foreground: {foreground};
            --border: {border};
            --ring: {primary};
            --radius: 0.5rem;
          }}
        }}

        * {{
          @apply border-border;
        }}

        body {{
          @apply bg-background text-foreground;
          font-feature-settings: "rlig" 1, "calt" 1;
        }}
    """)


def tsconfig_json() -> str:
    return json.dumps({
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "paths": {"@/*": ["./src/*"]}
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }, indent=2)


def postcss_config() -> str:
    return textwrap.dedent("""\
        module.exports = {
          plugins: {
            tailwindcss: {},
            autoprefixer: {},
          },
        };
    """)


def env_local_example() -> str:
    return textwrap.dedent("""\
        # Firebase client-side config (safe to expose to browser)
        NEXT_PUBLIC_FIREBASE_API_KEY=
        NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
        NEXT_PUBLIC_FIREBASE_PROJECT_ID=
        NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
        NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
        NEXT_PUBLIC_FIREBASE_APP_ID=

        # Server-side only
        GEMINI_API_KEY=
    """)


def firestore_rules() -> str:
    reference = Path(__file__).parent.parent / "reference" / "firebase_security_rules.txt"
    if reference.exists():
        return reference.read_text()
    return "rules_version = '2';\nservice cloud.firestore {\n  match /databases/{database}/documents {\n  }\n}"


def jest_config() -> str:
    return textwrap.dedent("""\
        const nextJest = require("next/jest");

        const createJestConfig = nextJest({ dir: "./" });

        const customJestConfig = {
          setupFilesAfterFramework: ["<rootDir>/jest.setup.ts"],
          testEnvironment: "jest-environment-jsdom",
        };

        module.exports = createJestConfig(customJestConfig);
    """)


def jest_setup() -> str:
    return 'import "@testing-library/jest-dom";\n'


def gitignore() -> str:
    return textwrap.dedent("""\
        node_modules/
        .next/
        .env.local
        .env
        out/
        dist/
        *.log
    """)


# ---------------------------------------------------------------------------
# Scaffold runner
# ---------------------------------------------------------------------------

FILES: dict[str, str] = {
    "package.json": package_json(),
    "tailwind.config.js": tailwind_config(),
    "next.config.js": next_config(),
    "tsconfig.json": tsconfig_json(),
    "postcss.config.js": postcss_config(),
    "jest.config.js": jest_config(),
    "jest.setup.ts": jest_setup(),
    ".gitignore": gitignore(),
    ".env.local.example": env_local_example(),
    "firestore.rules": firestore_rules(),
    "src/lib/firebase.ts": firebase_config_ts(),
    "src/lib/utils.ts": cn_util_ts(),
    "src/components/ui/button.tsx": button_component_tsx(),
    "src/pages/index.tsx": index_page_tsx(),
    "src/styles/globals.css": global_css(),
    "src/components/.gitkeep": "",
    "src/hooks/.gitkeep": "",
    "functions/.gitkeep": "",
}


def scaffold() -> None:
    print(f"Scaffolding project: {PROJECT_NAME}")
    print(f"Output directory:    {OUTPUT_DIR}")
    print(f"Primary color:       {_COLORS['primary']}")
    print(f"Font family:         {_FONTS['sans']}\n")

    for rel_path, content in FILES.items():
        target = OUTPUT_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        print(f"  created  {rel_path}")

    print(f"\nDone. {len(FILES)} files written to {OUTPUT_DIR}/")
    print("\nNext steps:")
    print("  1. cd into the directory")
    print("  2. cp .env.local.example .env.local && fill in Firebase config")
    print("  3. npm install")
    print("  4. npx shadcn-ui@latest init  (add more components as needed)")
    print("  5. npm run dev")


if __name__ == "__main__":
    scaffold()
