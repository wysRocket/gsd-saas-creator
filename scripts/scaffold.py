"""
scaffold.py — Generates a React/Next.js + Firebase project skeleton
from the rendered DESIGN.md and ARCHITECTURE.md files.

Usage:
    python scripts/scaffold.py [output_dir]

Output defaults to ./output/<project_name>/
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
# File content generators
# ---------------------------------------------------------------------------

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
            "next": "^14.0.0",
            "react": "^18.0.0",
            "react-dom": "^18.0.0",
            "firebase": "^10.0.0",
            "tailwindcss": "^3.4.0",
            "@tailwindcss/forms": "^0.5.0"
        },
        "devDependencies": {
            "@types/node": "^20.0.0",
            "@types/react": "^18.0.0",
            "jest": "^29.0.0",
            "@testing-library/react": "^14.0.0",
            "@testing-library/jest-dom": "^6.0.0",
            "typescript": "^5.0.0"
        }
    }, indent=2)


def tailwind_config() -> str:
    return textwrap.dedent("""\
        /** @type {import('tailwindcss').Config} */
        module.exports = {
          content: ["./src/**/*.{js,ts,jsx,tsx}"],
          theme: {
            extend: {},
          },
          plugins: [require("@tailwindcss/forms")],
        };
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


def index_page_tsx() -> str:
    return textwrap.dedent(f"""\
        import type {{ NextPage }} from "next";
        import Head from "next/head";

        const Home: NextPage = () => {{
          return (
            <>
              <Head>
                <title>{PROJECT_NAME}</title>
              </Head>
              <main className="flex min-h-screen flex-col items-center justify-center p-8">
                <h1 className="text-4xl font-bold">{PROJECT_NAME}</h1>
                <p className="mt-4 text-gray-500">Your SaaS is ready. Start building.</p>
              </main>
            </>
          );
        }};

        export default Home;
    """)


def global_css() -> str:
    return textwrap.dedent("""\
        @tailwind base;
        @tailwind components;
        @tailwind utilities;
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
    "jest.config.js": jest_config(),
    "jest.setup.ts": jest_setup(),
    ".gitignore": gitignore(),
    ".env.local.example": env_local_example(),
    "firestore.rules": firestore_rules(),
    "src/lib/firebase.ts": firebase_config_ts(),
    "src/pages/index.tsx": index_page_tsx(),
    "src/styles/globals.css": global_css(),
    "src/components/.gitkeep": "",
    "src/hooks/.gitkeep": "",
    "functions/.gitkeep": "",
}


def scaffold() -> None:
    print(f"Scaffolding project: {PROJECT_NAME}")
    print(f"Output directory: {OUTPUT_DIR}\n")

    for rel_path, content in FILES.items():
        target = OUTPUT_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        print(f"  created  {rel_path}")

    print(f"\nDone. {len(FILES)} files written to {OUTPUT_DIR}/")
    print("Next: cd into the directory, copy .env.local.example to .env.local, and run `npm install`")


if __name__ == "__main__":
    scaffold()
