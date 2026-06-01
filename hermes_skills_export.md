# Hermes Skills Export — MaxHermes skill_manage() Commands
# Generated from all 71 SKILL.md files in the hermes-agent skills/ directory.
# Copy individual blocks or the entire file into MaxHermes.

---

## APPLE

skill_manage(
    action="add",
    name="apple-notes",
    description="Read, create, search, and manage Apple Notes on macOS using the memo CLI. Use when the user wants to create a note, search notes, or view existing Apple Notes.",
    triggers=["apple notes", "create note", "search notes", "memo", "add to notes", "find note"],
    steps=[
        "Step 1: Set shorthand — MEMO='memo'",
        "Step 2: List all notes — memo list",
        "Step 3: Create a note — memo add 'Title' 'Body text'",
        "Step 4: Search notes — memo search 'keyword'",
        "Step 5: Read a note — memo get 'Note Title'",
        "Step 6: Delete a note — memo delete 'Note Title'",
    ]
)

---

skill_manage(
    action="add",
    name="apple-reminders",
    description="Create, complete, list, and delete Apple Reminders on macOS using the remindctl CLI. Use when the user wants to manage tasks or reminders in Apple Reminders.",
    triggers=["reminder", "reminders", "todo", "task", "remindctl", "set a reminder", "add reminder"],
    steps=[
        "Step 1: List all reminders — remindctl list",
        "Step 2: List by list name — remindctl list 'Groceries'",
        "Step 3: Add a reminder — remindctl add 'Buy milk' --list 'Groceries' --due '2026-06-01 10:00'",
        "Step 4: Complete a reminder — remindctl complete REMINDER_ID",
        "Step 5: Delete a reminder — remindctl delete REMINDER_ID",
    ]
)

---

skill_manage(
    action="add",
    name="imessage",
    description="Send iMessages/SMS and read conversations on macOS using the imsg CLI. Use when the user wants to send a text message, read a conversation, or list recent messages.",
    triggers=["imessage", "send message", "text", "sms", "imsg", "send text", "read messages", "message someone"],
    steps=[
        "Step 1: Send a message — imsg send '+15551234567' 'Hello!'",
        "Step 2: Read conversation — imsg read '+15551234567' --limit 20",
        "Step 3: List recent conversations — imsg list",
        "Step 4: Search messages — imsg search 'keyword'",
        "Step 5: Send to contact by name — imsg send 'John Doe' 'Hello!'",
    ]
)

---

skill_manage(
    action="add",
    name="findmy",
    description="Locate Apple devices, AirTags, and people using Find My on macOS via AppleScript and screenshots. Use when the user wants to find the location of a device or AirTag.",
    triggers=["find my", "findmy", "locate device", "airtag", "where is my", "track device", "find iphone"],
    steps=[
        "Step 1: Open Find My app via AppleScript",
        "Step 2: Take a screenshot to capture current device locations",
        "Step 3: Parse screenshot to extract device names and locations",
        "Step 4: Report location information to the user",
        "Step 5: For AirTags — select AirTag from list and read coordinates",
    ]
)

---

## AUTONOMOUS AI AGENTS

skill_manage(
    action="add",
    name="claude-code",
    description="Run Claude Code as an autonomous coding agent (Anthropic's CLI). Two modes: print mode for one-shot tasks (-p flag), interactive mode via tmux for multi-turn sessions. Use when delegating a coding task to a Claude subagent.",
    triggers=["claude code", "run claude", "claude agent", "coding agent", "delegate coding", "claude -p", "autonomous coding"],
    steps=[
        "Step 1 (print mode): claude -p 'task description' --allowedTools 'Bash,Read,Edit,Write'",
        "Step 2 (interactive mode): Start tmux session — tmux new-session -d -s claude",
        "Step 3 (interactive mode): Launch Claude in tmux — tmux send-keys -t claude 'claude' Enter",
        "Step 4 (interactive mode): Send instructions — tmux send-keys -t claude 'task description' Enter",
        "Step 5: Monitor output — tmux attach -t claude",
        "Step 6: Retrieve results from the session or output files",
    ]
)

---

skill_manage(
    action="add",
    name="codex",
    description="Run OpenAI Codex as an autonomous coding agent using the codex CLI. Requires a git repository. Use when delegating coding tasks to an OpenAI-powered coding agent.",
    triggers=["codex", "openai codex", "codex agent", "codex exec", "run codex"],
    steps=[
        "Step 1: Ensure the working directory is a git repository",
        "Step 2: Run a task — codex exec 'task description'",
        "Step 3: For approval mode — codex exec --approval 'task description'",
        "Step 4: Review the generated diff — git diff",
        "Step 5: Accept or reject changes",
    ]
)

---

skill_manage(
    action="add",
    name="hermes-agent",
    description="Complete reference for configuring, spawning, and managing Hermes Agent instances. Covers setup, config.yaml, multi-agent spawning, CLI usage, gateway mode, skills, and environment variables.",
    triggers=["hermes", "hermes setup", "hermes config", "spawn agent", "hermes gateway", "hermes cli", "multi-agent"],
    steps=[
        "Step 1: Install — pip install hermes-agent or from source",
        "Step 2: Configure — edit ~/.hermes/config.yaml (model, system_prompt, skills)",
        "Step 3: Set API keys in ~/.hermes/.env",
        "Step 4: Run CLI — hermes 'your task'",
        "Step 5: Run gateway — hermes gateway (for Telegram/Discord/API)",
        "Step 6: Spawn subagents — use delegate_task() in agent context",
        "Step 7: Manage skills — hermes skills list / install / enable",
    ]
)

---

skill_manage(
    action="add",
    name="opencode",
    description="Run OpenCode as an autonomous coding agent using the opencode CLI. Supports multiple LLM backends. Use when delegating coding tasks to the OpenCode agent.",
    triggers=["opencode", "open code", "opencode agent", "opencode run"],
    steps=[
        "Step 1: Ensure opencode is installed — opencode --version",
        "Step 2: Run a task — opencode run 'task description'",
        "Step 3: Specify a model — opencode run --model claude-sonnet 'task'",
        "Step 4: Review output and generated files",
        "Step 5: Commit accepted changes — git add -A && git commit -m 'description'",
    ]
)

---

## CREATIVE

skill_manage(
    action="add",
    name="architecture-diagram",
    description="Generate dark-themed HTML/SVG architecture diagrams. Creates self-contained HTML files with layered system diagrams. Use when the user wants a visual architecture overview.",
    triggers=["architecture diagram", "system diagram", "draw architecture", "infrastructure diagram", "svg diagram"],
    steps=[
        "Step 1: Identify components and their relationships",
        "Step 2: Define layers (frontend, backend, database, infra, etc.)",
        "Step 3: Generate SVG/HTML with dark theme and labeled boxes",
        "Step 4: Add arrows and connection lines between components",
        "Step 5: Save as self-contained .html file",
        "Step 6: Open in browser to verify rendering",
    ]
)

---

skill_manage(
    action="add",
    name="ascii-art",
    description="Create ASCII art, banners, and animations using 9 tools: pyfiglet, cowsay, boxes, toilet, lolcat, figlet, jp2a, aalib, and caca. Use for text banners, artistic text, or fun ASCII output.",
    triggers=["ascii art", "ascii banner", "ascii text", "pyfiglet", "cowsay", "figlet", "text art", "ascii animation"],
    steps=[
        "Step 1: Install tools — pip install pyfiglet; apt install cowsay boxes toilet",
        "Step 2: Text banner — python3 -c \"import pyfiglet; print(pyfiglet.figlet_format('Hello'))\"",
        "Step 3: Cowsay — cowsay 'Hello world'",
        "Step 4: Boxes — echo 'text' | boxes -d stone",
        "Step 5: Colored art — echo 'text' | toilet --gay",
        "Step 6: Image to ASCII — jp2a image.jpg --width=80",
    ]
)

---

skill_manage(
    action="add",
    name="ascii-video",
    description="Create ASCII video animations in 6 modes: video-to-ASCII, audio-reactive, generative, hybrid, lyrics-sync, and TTS-driven. Use for creative terminal animations or artistic video conversions.",
    triggers=["ascii video", "ascii animation", "video to ascii", "terminal animation", "ascii movie"],
    steps=[
        "Step 1: Choose mode — video-to-ASCII, generative, audio-reactive, hybrid, lyrics, or TTS",
        "Step 2 (video mode): Convert — python ascii_video.py input.mp4 --output output.txt",
        "Step 3 (generative mode): Generate — python ascii_video.py --mode generative --duration 10",
        "Step 4 (audio-reactive mode): python ascii_video.py --mode audio --input audio.mp3",
        "Step 5: Play the result in terminal or save as video",
    ]
)

---

skill_manage(
    action="add",
    name="baoyu-infographic",
    description="Create visual summary infographics with 21 layouts and 21 design styles. Generates a single rich HTML infographic from any content. Trigger when user requests 'infographic' or '信息图'.",
    triggers=["infographic", "信息图", "visual summary", "create infographic", "make infographic", "visual chart"],
    steps=[
        "Step 1: Extract key information from the source content",
        "Step 2: Choose layout (timeline, comparison, stats, process, etc.)",
        "Step 3: Choose design style (minimal, tech, corporate, vibrant, etc.)",
        "Step 4: Generate single-file HTML with embedded CSS and data",
        "Step 5: Verify visual rendering in browser",
    ]
)

---

skill_manage(
    action="add",
    name="ideation",
    description="Constraint-driven creative project ideation and brainstorming. Generates novel, specific, actionable project ideas using creative constraints. Use when the user wants project ideas or creative inspiration.",
    triggers=["ideation", "brainstorm", "project ideas", "creative ideas", "idea generation", "what should I build"],
    steps=[
        "Step 1: Gather constraints (domain, tools, time, audience)",
        "Step 2: Apply creative constraint techniques (inversion, combination, extreme scale)",
        "Step 3: Generate 5-10 candidate ideas",
        "Step 4: Evaluate ideas against constraints",
        "Step 5: Develop top ideas with specific details and next steps",
    ]
)

---

skill_manage(
    action="add",
    name="excalidraw",
    description="Generate Excalidraw diagram files (.excalidraw JSON) for flowcharts, architecture diagrams, wireframes, and mind maps. Files open directly in Excalidraw.",
    triggers=["excalidraw", "flowchart", "diagram", "draw diagram", "wireframe", "mind map", "flow diagram"],
    steps=[
        "Step 1: Identify diagram type (flowchart, architecture, wireframe, mind map)",
        "Step 2: Define nodes and connections",
        "Step 3: Generate valid .excalidraw JSON with elements array",
        "Step 4: Set positions, sizes, colors, and styles for each element",
        "Step 5: Save as filename.excalidraw",
        "Step 6: Open in Excalidraw to verify",
    ]
)

---

skill_manage(
    action="add",
    name="manim-video",
    description="Create mathematical and educational animations using Manim in 7 modes: concept explainer, equation derivation, algorithm visualization, data animation, geometric proof, physics simulation, and statistics. Outputs MP4 video.",
    triggers=["manim", "math animation", "equation animation", "educational video", "visualize algorithm", "animate math"],
    steps=[
        "Step 1: Install — pip install manim",
        "Step 2: Choose mode (concept, equation, algorithm, data, geometry, physics, statistics)",
        "Step 3: Write Manim Scene class with animations",
        "Step 4: Render — manim -pql scene.py SceneName",
        "Step 5: For high quality — manim -pqh scene.py SceneName",
        "Step 6: Output MP4 is in media/videos/ directory",
    ]
)

---

skill_manage(
    action="add",
    name="p5js",
    description="Create generative art and interactive sketches using p5.js in 7 modes: generative art, particle systems, data visualization, interactive, WebGL 3D, shader art, and simulations. Outputs HTML files.",
    triggers=["p5js", "p5.js", "generative art", "creative coding", "particle system", "canvas art", "webgl art", "interactive art"],
    steps=[
        "Step 1: Choose mode (generative, particles, dataviz, interactive, 3D, shaders, simulation)",
        "Step 2: Write p5.js sketch with setup() and draw() functions",
        "Step 3: Embed in self-contained HTML with p5.js CDN",
        "Step 4: Add interactivity (mouse, keyboard) if needed",
        "Step 5: Save as .html and open in browser",
        "Step 6: Iterate on parameters for desired visual output",
    ]
)

---

skill_manage(
    action="add",
    name="pixel-art",
    description="Generate retro pixel art in 14 presets (NES, SNES, Game Boy, Atari, CGA, EGA, etc.). Creates HTML canvas output with authentic color palettes. Use for retro game sprites, pixel icons, or nostalgic art.",
    triggers=["pixel art", "nes art", "game boy art", "retro art", "sprite", "pixel sprite", "8-bit art", "16-bit art", "snes", "atari"],
    steps=[
        "Step 1: Choose preset (nes, snes, gameboy, gameboy_color, atari, cga, ega, etc.)",
        "Step 2: Define pixel grid dimensions (e.g., 16x16, 32x32)",
        "Step 3: Apply preset color palette constraints",
        "Step 4: Generate HTML canvas with pixelated rendering",
        "Step 5: Add animation frames if needed",
        "Step 6: Save as .html for display",
    ]
)

---

skill_manage(
    action="add",
    name="popular-web-designs",
    description="Build web pages inspired by 54 popular design systems (Linear, Vercel, Stripe, Apple, GitHub, Notion, etc.). Generates complete HTML/CSS. Trigger when user says 'design like X' or 'looks like X'.",
    triggers=["design like", "looks like", "build a page like", "inspired by", "linear design", "stripe design", "apple design", "notion design", "vercel design"],
    steps=[
        "Step 1: Identify the target design system from the 54 available",
        "Step 2: Extract key design tokens (colors, typography, spacing, border-radius)",
        "Step 3: Generate HTML structure matching the design system's layout",
        "Step 4: Write CSS using the extracted design tokens",
        "Step 5: Add interactive elements (hover, focus, transitions)",
        "Step 6: Test responsiveness and visual fidelity",
    ]
)

---

skill_manage(
    action="add",
    name="songwriting-and-ai-music",
    description="Write song lyrics and generate Suno AI music prompts. Covers verse/chorus structure, rhyme schemes, style transfer, and Suno meta-tag engineering for text-to-music generation.",
    triggers=["write a song", "song lyrics", "suno", "music generation", "ai music", "parody song", "song about", "write lyrics"],
    steps=[
        "Step 1: Define song concept, genre, mood, and target audience",
        "Step 2: Write verse and chorus structure with rhyme scheme",
        "Step 3: Craft a hook and bridge",
        "Step 4: Generate Suno prompt with style tags [Genre: ][Mood: ][Instruments: ]",
        "Step 5: Add Suno meta-tags for structure ([Verse][Chorus][Bridge][Outro])",
        "Step 6: Submit to Suno and iterate on lyrics/prompt",
    ]
)

---

## DATA SCIENCE

skill_manage(
    action="add",
    name="jupyter-live-kernel",
    description="Run interactive Jupyter notebooks with a live kernel using hamelnb via uv. Enables iterative data analysis, visualization, and REPL-style code execution. Use for data science workflows.",
    triggers=["jupyter", "notebook", "jupyter notebook", "data analysis", "interactive python", "live kernel", "repl"],
    steps=[
        "Step 1: Install — uv tool install hamelnb",
        "Step 2: Start kernel — hamelnb start",
        "Step 3: Execute cells — hamelnb run 'import pandas as pd; df = pd.read_csv(\"data.csv\")'",
        "Step 4: Visualize — hamelnb run 'df.plot(); plt.savefig(\"plot.png\")'",
        "Step 5: Save notebook — hamelnb save notebook.ipynb",
        "Step 6: Stop kernel — hamelnb stop",
    ]
)

---

## DEVOPS

skill_manage(
    action="add",
    name="webhook-subscriptions",
    description="Subscribe to and manage event webhooks in Hermes using the hermes webhook CLI. Use for automation triggers, push notifications, and integrations with external services.",
    triggers=["webhook", "subscribe to events", "hermes webhook", "event subscription", "push notification", "automation trigger"],
    steps=[
        "Step 1: List available events — hermes webhook list-events",
        "Step 2: Subscribe to an event — hermes webhook subscribe --event 'message.received' --url 'https://...'",
        "Step 3: List subscriptions — hermes webhook subscriptions",
        "Step 4: Test a webhook — hermes webhook test SUBSCRIPTION_ID",
        "Step 5: Delete a subscription — hermes webhook unsubscribe SUBSCRIPTION_ID",
    ]
)

---

## DOGFOOD / QA

skill_manage(
    action="add",
    name="dogfood",
    description="5-phase systematic web QA workflow for testing Hermes web features in a browser. Covers setup, golden-path testing, edge cases, regression checks, and bug reporting.",
    triggers=["qa", "quality assurance", "test the web", "dogfood", "test in browser", "browser testing", "web testing"],
    steps=[
        "Step 1: Setup — identify target URL and test scope",
        "Step 2: Golden path — test the primary happy-path user flow",
        "Step 3: Edge cases — test boundary inputs, empty states, errors",
        "Step 4: Regression — verify previously known issues are fixed",
        "Step 5: Bug report — document findings with steps to reproduce, screenshots",
    ]
)

---

## EMAIL

skill_manage(
    action="add",
    name="himalaya",
    description="Read, send, reply to, and manage emails from the terminal using the himalaya CLI over IMAP/SMTP. Supports multiple accounts. Use for email workflows without a GUI.",
    triggers=["email", "check email", "send email", "read email", "himalaya", "imap", "inbox"],
    steps=[
        "Step 1: Configure account in ~/.config/himalaya/config.toml (IMAP + SMTP settings)",
        "Step 2: List inbox — himalaya envelope list",
        "Step 3: Read message — himalaya message read MESSAGE_ID",
        "Step 4: Send email — himalaya message send --to user@example.com --subject 'Subject' --body 'Body'",
        "Step 5: Reply — himalaya message reply MESSAGE_ID",
        "Step 6: Search — himalaya envelope list --query 'from:boss@example.com'",
    ]
)

---

## GAMING

skill_manage(
    action="add",
    name="pokemon-player",
    description="Play Pokémon games headlessly using the PyBoy Game Boy emulator via the pokemon-agent framework. Supports automated gameplay, state saving, and memory reading.",
    triggers=["pokemon", "play pokemon", "game boy", "pyboy", "pokemon agent", "emulator", "pokemon game"],
    steps=[
        "Step 1: Install — pip install pokemon-agent pyboy",
        "Step 2: Load ROM — agent = PokemonAgent('pokemon_red.gb')",
        "Step 3: Start game — agent.start()",
        "Step 4: Issue actions — agent.press('A') / agent.move('up')",
        "Step 5: Read game state — agent.get_state() (party, location, items)",
        "Step 6: Save state — agent.save_state('checkpoint.state')",
    ]
)

---

skill_manage(
    action="add",
    name="minecraft-modpack-server",
    description="Set up and manage a Minecraft modpack server using NeoForge or Forge. Covers installation, mod management, server configuration, and startup. Use when the user wants to run a Minecraft server.",
    triggers=["minecraft", "minecraft server", "modpack", "neoforge", "forge server", "minecraft mods"],
    steps=[
        "Step 1: Download NeoForge installer from neoforged.net",
        "Step 2: Install server — java -jar neoforge-installer.jar --installServer",
        "Step 3: Accept EULA — echo 'eula=true' > eula.txt",
        "Step 4: Add mods to /mods directory",
        "Step 5: Configure server.properties (difficulty, gamemode, max-players)",
        "Step 6: Start server — java -Xmx4G -jar server.jar nogui",
    ]
)

---

## GITHUB

skill_manage(
    action="add",
    name="codebase-inspection",
    description="Analyze codebase metrics (lines of code, language breakdown, file counts) using pygount. Use when the user wants to understand the size, composition, or complexity of a codebase.",
    triggers=["codebase stats", "lines of code", "loc", "code metrics", "codebase analysis", "pygount", "code size"],
    steps=[
        "Step 1: Install — pip install pygount",
        "Step 2: Count lines — pygount --format=summary .",
        "Step 3: Language breakdown — pygount --format=cloc-xml . > stats.xml",
        "Step 4: Specific directory — pygount --format=summary src/",
        "Step 5: Export to CSV — pygount --format=csv . > stats.csv",
        "Step 6: Visualize — parse CSV/XML for charts",
    ]
)

---

skill_manage(
    action="add",
    name="github-auth",
    description="Set up and verify GitHub authentication via gh CLI, SSH keys, or HTTPS tokens. Detects existing auth and guides through setup. Use before any GitHub operations.",
    triggers=["github auth", "github login", "gh auth", "git authentication", "ssh key github", "github token"],
    steps=[
        "Step 1: Check existing auth — gh auth status",
        "Step 2 (gh CLI): Authenticate — gh auth login (follow prompts)",
        "Step 3 (SSH): Generate key — ssh-keygen -t ed25519 -C 'email@example.com'",
        "Step 4 (SSH): Add to GitHub — copy ~/.ssh/id_ed25519.pub to GitHub Settings > SSH keys",
        "Step 5 (token): Set — git config --global credential.helper store",
        "Step 6: Verify — gh api /user && git clone test",
    ]
)

---

skill_manage(
    action="add",
    name="github-code-review",
    description="Perform code reviews on GitHub pull requests using the gh CLI and MCP tools. Supports pre-push review of local changes and reviewing open PRs with inline comments.",
    triggers=["code review", "review pr", "review pull request", "github review", "pr review", "review code"],
    steps=[
        "Step 1: Fetch PR diff — gh pr diff PR_NUMBER",
        "Step 2: Read changed files — gh pr view PR_NUMBER --json files",
        "Step 3: Analyze for bugs, security issues, style",
        "Step 4: Post inline comment — gh pr review PR_NUMBER --comment -b 'feedback'",
        "Step 5: Request changes — gh pr review PR_NUMBER --request-changes -b 'summary'",
        "Step 6: Approve — gh pr review PR_NUMBER --approve -b 'LGTM'",
    ]
)

---

skill_manage(
    action="add",
    name="github-issues",
    description="Create, search, update, label, assign, and close GitHub issues using the gh CLI and GitHub API. Use for issue management and project tracking.",
    triggers=["github issue", "create issue", "open issue", "bug report", "feature request", "gh issue", "list issues"],
    steps=[
        "Step 1: List issues — gh issue list --repo owner/repo",
        "Step 2: Create issue — gh issue create --title 'Title' --body 'Description' --label bug",
        "Step 3: View issue — gh issue view ISSUE_NUMBER",
        "Step 4: Update issue — gh issue edit ISSUE_NUMBER --add-label enhancement",
        "Step 5: Assign — gh issue edit ISSUE_NUMBER --add-assignee username",
        "Step 6: Close — gh issue close ISSUE_NUMBER --comment 'Fixed in #PR'",
    ]
)

---

skill_manage(
    action="add",
    name="github-pr-workflow",
    description="Full pull request lifecycle management: create branches, commit, push, open PRs, handle reviews, merge, and clean up. Uses gh CLI. Use for any GitHub PR workflow.",
    triggers=["pull request", "pr workflow", "open pr", "create pr", "merge pr", "github workflow", "submit changes"],
    steps=[
        "Step 1: Create branch — git checkout -b feature/branch-name",
        "Step 2: Make changes and commit — git add . && git commit -m 'feat: description'",
        "Step 3: Push — git push -u origin feature/branch-name",
        "Step 4: Open PR — gh pr create --title 'Title' --body 'Description' --base main",
        "Step 5: Monitor CI — gh pr checks PR_NUMBER",
        "Step 6: Merge — gh pr merge PR_NUMBER --squash",
        "Step 7: Clean up — git branch -d feature/branch-name",
    ]
)

---

skill_manage(
    action="add",
    name="github-repo-management",
    description="Manage GitHub repositories: clone, create, fork, configure secrets, manage releases, and set branch protection. Uses gh CLI and git.",
    triggers=["github repo", "create repository", "clone repo", "fork repo", "repo management", "github secrets", "github release"],
    steps=[
        "Step 1: Clone — gh repo clone owner/repo",
        "Step 2: Create repo — gh repo create my-repo --public --clone",
        "Step 3: Fork — gh repo fork owner/repo --clone",
        "Step 4: Set secret — gh secret set SECRET_NAME --body 'value'",
        "Step 5: Create release — gh release create v1.0.0 --notes 'Release notes'",
        "Step 6: Set branch protection — gh api repos/owner/repo/branches/main/protection -X PUT -f ...",
    ]
)

---

## MCP

skill_manage(
    action="add",
    name="native-mcp",
    description="Use Hermes's built-in MCP (Model Context Protocol) client to connect to MCP servers via stdio or HTTP transports. Use when integrating external tools, databases, or services via MCP.",
    triggers=["mcp", "mcp server", "model context protocol", "mcp tool", "mcp integration", "connect mcp"],
    steps=[
        "Step 1: Configure MCP server in ~/.hermes/config.yaml under mcp_servers",
        "Step 2 (stdio): Add server — name: my-tool, command: 'my-mcp-server', args: [...]",
        "Step 3 (HTTP): Add server — name: my-tool, url: 'http://localhost:3000'",
        "Step 4: Restart Hermes to load the new MCP server",
        "Step 5: Tools from the MCP server are now available as mcp__servername__toolname",
        "Step 6: Call tools — mcp__my-tool__some_function(param='value')",
    ]
)

---

## MEDIA

skill_manage(
    action="add",
    name="gif-search",
    description="Search and retrieve GIFs from Tenor using the Tenor API via curl. Returns GIF URLs that can be shared in chat. Requires TENOR_API_KEY environment variable.",
    triggers=["gif", "find gif", "search gif", "tenor", "animated gif", "reaction gif"],
    steps=[
        "Step 1: Set API key — export TENOR_API_KEY=your_key",
        "Step 2: Search GIFs — curl 'https://tenor.googleapis.com/v2/search?q=QUERY&key=$TENOR_API_KEY&limit=5'",
        "Step 3: Parse JSON response to extract GIF URLs",
        "Step 4: Return top GIF URL(s) to the user",
        "Step 5: For trending GIFs — replace /search with /featured",
    ]
)

---

skill_manage(
    action="add",
    name="heartmula",
    description="Generate AI music using Heartmula, an open-source text-to-music system similar to Suno. Use when the user wants to generate music without using the Suno API.",
    triggers=["heartmula", "generate music", "ai music", "text to music", "music from text", "local music generation"],
    steps=[
        "Step 1: Install Heartmula and dependencies",
        "Step 2: Provide text description of desired music",
        "Step 3: Set generation parameters (duration, style, tempo)",
        "Step 4: Run generation — heartmula generate --prompt 'upbeat jazz piano' --duration 30",
        "Step 5: Output audio file (WAV/MP3) saved to disk",
    ]
)

---

skill_manage(
    action="add",
    name="songsee",
    description="Create audio visualizations, spectrograms, and audio feature analysis charts from audio files. Use when the user wants to visualize audio or music data.",
    triggers=["spectrogram", "audio visualization", "visualize audio", "songsee", "audio features", "waveform", "frequency plot"],
    steps=[
        "Step 1: Install — pip install songsee librosa matplotlib",
        "Step 2: Generate spectrogram — songsee spectrogram audio.mp3",
        "Step 3: Waveform plot — songsee waveform audio.wav",
        "Step 4: Feature analysis — songsee features audio.mp3 --features mfcc,chroma,spectral",
        "Step 5: Save visualization — output PNG saved automatically",
    ]
)

---

skill_manage(
    action="add",
    name="youtube-content",
    description="Fetch YouTube video transcripts and transform them (summarize, extract key points, translate, create notes). Uses YouTube Transcript API. No API key needed for public videos.",
    triggers=["youtube transcript", "youtube summary", "youtube video", "get transcript", "summarize video", "youtube notes"],
    steps=[
        "Step 1: Extract video ID from YouTube URL",
        "Step 2: Fetch transcript — pip install youtube-transcript-api",
        "Step 3: Get transcript — from youtube_transcript_api import YouTubeTranscriptApi; t = YouTubeTranscriptApi.get_transcript('VIDEO_ID')",
        "Step 4: Join text — full_text = ' '.join([x['text'] for x in t])",
        "Step 5: Transform — summarize, extract key points, or format as notes",
    ]
)

---

## MLOPS — EVALUATION

skill_manage(
    action="add",
    name="evaluating-llms-harness",
    description="Evaluate LLMs on 60+ standardized benchmarks (MMLU, HellaSwag, ARC, TruthfulQA, GSM8K, etc.) using the EleutherAI LM Evaluation Harness. Use when benchmarking a language model.",
    triggers=["evaluate llm", "benchmark model", "lm eval", "mmlu", "hellaswag", "arc benchmark", "model evaluation", "lm-evaluation-harness"],
    steps=[
        "Step 1: Install — pip install lm-eval",
        "Step 2: Evaluate HuggingFace model — lm_eval --model hf --model_args pretrained=MODEL_NAME --tasks mmlu --device cuda",
        "Step 3: Evaluate OpenAI model — lm_eval --model openai-completions --model_args model=gpt-4 --tasks gsm8k",
        "Step 4: Multiple tasks — --tasks mmlu,hellaswag,arc_easy,arc_challenge",
        "Step 5: Save results — --output_path results/",
        "Step 6: Review JSON results for accuracy scores per task",
    ]
)

---

skill_manage(
    action="add",
    name="weights-and-biases",
    description="Track ML experiments, log metrics/artifacts, visualize training runs, and manage hyperparameter sweeps using Weights & Biases (W&B). Full integration with PyTorch, HuggingFace, and custom training loops.",
    triggers=["wandb", "weights and biases", "experiment tracking", "log metrics", "training dashboard", "mlops tracking", "hyperparameter sweep"],
    steps=[
        "Step 1: Install — pip install wandb",
        "Step 2: Login — wandb login (paste API key from wandb.ai)",
        "Step 3: Initialize run — wandb.init(project='my-project', config={...})",
        "Step 4: Log metrics — wandb.log({'loss': 0.5, 'accuracy': 0.92})",
        "Step 5: Log artifacts — wandb.log_artifact('model.pt', name='model', type='model')",
        "Step 6: HuggingFace integration — add report_to='wandb' to TrainingArguments",
        "Step 7: View results at wandb.ai/your-username/my-project",
    ]
)

---

## MLOPS — HUGGINGFACE HUB

skill_manage(
    action="add",
    name="huggingface-hub",
    description="Manage HuggingFace Hub models, datasets, and spaces using the hf CLI. Upload/download models, search the hub, and manage repositories. Use for any HuggingFace Hub interaction.",
    triggers=["huggingface", "hf hub", "hf cli", "upload model", "download model", "huggingface hub", "push to hub", "hf dataset"],
    steps=[
        "Step 1: Install — pip install huggingface_hub",
        "Step 2: Login — huggingface-cli login (or hf login)",
        "Step 3: Download model — hf download org/model --local-dir ./model",
        "Step 4: Upload model — hf upload org/model ./local-dir",
        "Step 5: Search — hf search 'llama 3'",
        "Step 6: List repos — hf repo list",
        "Step 7: Create dataset — hf repo create my-dataset --type dataset",
    ]
)

---

## MLOPS — INFERENCE

skill_manage(
    action="add",
    name="llama-cpp",
    description="Run LLM inference with llama.cpp using GGUF quantized models. Supports CPU, Metal (Apple Silicon), and CUDA. Full workflow: download GGUF, run server, benchmark. Use for local/offline LLM inference.",
    triggers=["llama.cpp", "llama cpp", "gguf", "quantized model", "cpu inference", "local llm", "llama server", "ollama alternative"],
    steps=[
        "Step 1: Install — pip install llama-cpp-python (or build from source for GPU)",
        "Step 2: Download GGUF model from HuggingFace",
        "Step 3: Run inference — llama-cli -m model.gguf -p 'Prompt here' -n 512",
        "Step 4: Start server — llama-server -m model.gguf --port 8080",
        "Step 5: Call API — curl http://localhost:8080/v1/chat/completions -d '{...}'",
        "Step 6: Quantize — llama-quantize model-f16.gguf model-q4.gguf Q4_K_M",
    ]
)

---

skill_manage(
    action="add",
    name="obliteratus",
    description="Remove refusal behaviors from open-weight LLMs using abliteration (weight modification) via the Obliteratus CLI. 9 techniques. AGPL-3.0. Use only on models you have rights to modify.",
    triggers=["obliteratus", "abliteration", "remove refusals", "uncensor model", "refusal removal", "uncensoring", "jailbreak weights"],
    steps=[
        "Step 1: Install — pip install obliteratus (requires GPU + VRAM)",
        "Step 2: Choose technique (activation_steering, weight_delta, etc.)",
        "Step 3: Run — obliteratus run --model org/model-name --technique weight_delta",
        "Step 4: Test output — compare before/after on refusal prompts",
        "Step 5: Save modified model — obliteratus save --output ./modified-model",
        "Step 6: Push to HuggingFace if sharing — hf upload org/model-abliterated ./modified-model",
        "WARNING: AGPL-3.0 license — check model license before redistributing",
    ]
)

---

skill_manage(
    action="add",
    name="outlines",
    description="Generate structured LLM outputs constrained to JSON Schema, Pydantic models, regex, or grammars using Outlines. FSM-based constrained generation guarantees valid output format.",
    triggers=["outlines", "structured generation", "json schema output", "constrained generation", "pydantic output", "structured llm output", "guaranteed json"],
    steps=[
        "Step 1: Install — pip install outlines",
        "Step 2: Load model — model = outlines.models.transformers('org/model')",
        "Step 3 (JSON Schema): Define schema as Pydantic model or dict",
        "Step 4 (JSON Schema): Generate — generator = outlines.generate.json(model, schema); result = generator(prompt)",
        "Step 5 (Regex): generator = outlines.generate.regex(model, pattern); result = generator(prompt)",
        "Step 6 (Choice): generator = outlines.generate.choice(model, ['A','B','C']); result = generator(prompt)",
    ]
)

---

skill_manage(
    action="add",
    name="serving-llms-vllm",
    description="Serve LLMs at high throughput using vLLM with PagedAttention. OpenAI-compatible API. Supports tensor parallelism, continuous batching, and quantization. Use for production LLM serving.",
    triggers=["vllm", "llm serving", "llm api", "serve model", "openai compatible", "llm inference server", "high throughput llm"],
    steps=[
        "Step 1: Install — pip install vllm",
        "Step 2: Start server — vllm serve org/model-name --port 8000",
        "Step 3: Multi-GPU — vllm serve org/model --tensor-parallel-size 4",
        "Step 4: With quantization — vllm serve org/model --quantization awq",
        "Step 5: Call API — curl http://localhost:8000/v1/chat/completions -d '{\"model\":\"...\", \"messages\":[...]}'",
        "Step 6: Python client — use openai Python SDK with base_url='http://localhost:8000/v1'",
    ]
)

---

## MLOPS — MODELS

skill_manage(
    action="add",
    name="audiocraft-audio-generation",
    description="Generate music and sound effects from text using Meta's AudioCraft (MusicGen, AudioGen, EnCodec). Supports melody conditioning, stereo output, and style transfer. Use for text-to-music or text-to-audio generation.",
    triggers=["musicgen", "audiogen", "audiocraft", "text to music", "generate music", "music from text", "sound effects generation", "audio generation"],
    steps=[
        "Step 1: Install — pip install audiocraft (or pip install transformers)",
        "Step 2: Load model — model = MusicGen.get_pretrained('facebook/musicgen-medium')",
        "Step 3: Set params — model.set_generation_params(duration=30, top_k=250, temperature=1.0)",
        "Step 4: Generate — wav = model.generate(['upbeat electronic dance music'])",
        "Step 5: Save — torchaudio.save('output.wav', wav[0].cpu(), sample_rate=32000)",
        "Step 6 (melody): model.generate_with_chroma(descriptions, melody, sr)",
    ]
)

---

skill_manage(
    action="add",
    name="segment-anything-model",
    description="Zero-shot image segmentation using Meta's SAM (Segment Anything Model). Supports point, box, and automatic prompts. Use when segmenting objects in images without task-specific training.",
    triggers=["segment anything", "sam", "image segmentation", "object segmentation", "zero-shot segmentation", "segment objects", "mask generation"],
    steps=[
        "Step 1: Install — pip install segment-anything (or pip install transformers)",
        "Step 2: Download checkpoint — wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
        "Step 3: Load model — sam = sam_model_registry['vit_h'](checkpoint='sam_vit_h_4b8939.pth'); sam.to('cuda')",
        "Step 4: Set image — predictor = SamPredictor(sam); predictor.set_image(image)",
        "Step 5 (point): masks, scores, _ = predictor.predict(point_coords=np.array([[x,y]]), point_labels=np.array([1]))",
        "Step 6 (box): masks, scores, _ = predictor.predict(box=np.array([x1,y1,x2,y2]))",
        "Step 7 (auto): mask_generator = SamAutomaticMaskGenerator(sam); masks = mask_generator.generate(image)",
    ]
)

---

## MLOPS — RESEARCH

skill_manage(
    action="add",
    name="dspy",
    description="Build and optimize AI systems declaratively using DSPy (Stanford NLP). Automatic prompt optimization, modular RAG systems, agents, and classifiers. Use when building complex multi-stage LLM pipelines.",
    triggers=["dspy", "declarative llm", "prompt optimization", "dspy optimizer", "rag pipeline", "llm programming", "automatic prompting"],
    steps=[
        "Step 1: Install — pip install dspy",
        "Step 2: Configure LM — lm = dspy.Claude(model='claude-sonnet-4-6'); dspy.settings.configure(lm=lm)",
        "Step 3: Define signature — class QA(dspy.Signature): question = dspy.InputField(); answer = dspy.OutputField()",
        "Step 4: Create module — qa = dspy.ChainOfThought(QA)",
        "Step 5: Use module — response = qa(question='What is Paris?')",
        "Step 6: Optimize — optimizer = BootstrapFewShot(metric=validate); optimized = optimizer.compile(qa, trainset=data)",
        "Step 7: Save — optimized.save('model.json')",
    ]
)

---

## MLOPS — TRAINING

skill_manage(
    action="add",
    name="axolotl",
    description="Fine-tune LLMs with Axolotl using YAML configuration. Supports 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal, DeepSpeed, and FSDP. Use when fine-tuning with a YAML-driven approach.",
    triggers=["axolotl", "yaml fine-tuning", "axolotl training", "lora training", "qlora training", "fine-tune yaml"],
    steps=[
        "Step 1: Install — pip install axolotl",
        "Step 2: Create config YAML with model, dataset, and training params",
        "Step 3: Configure LoRA — lora_r: 16, lora_alpha: 32, lora_target_modules: [q_proj, v_proj]",
        "Step 4: Preprocess — python -m axolotl.cli.preprocess config.yaml",
        "Step 5: Train — accelerate launch -m axolotl.cli.train config.yaml",
        "Step 6: Evaluate — python -m axolotl.cli.evaluate config.yaml",
        "Step 7: Merge LoRA — python -m axolotl.cli.merge_lora config.yaml",
    ]
)

---

skill_manage(
    action="add",
    name="fine-tuning-with-trl",
    description="Post-train and align LLMs using TRL (Transformer Reinforcement Learning). Supports SFT, DPO, PPO, GRPO, and reward model training. Full RLHF pipeline. Use for instruction tuning or preference alignment.",
    triggers=["trl", "rlhf", "sft trainer", "dpo", "ppo training", "grpo", "reward model", "preference alignment", "instruction tuning", "fine-tune trl"],
    steps=[
        "Step 1: Install — pip install trl transformers datasets peft accelerate",
        "Step 2 (SFT): trainer = SFTTrainer(model='Qwen/Qwen2.5-0.5B', train_dataset=dataset); trainer.train()",
        "Step 3 (DPO): config = DPOConfig(output_dir='model-dpo', beta=0.1); trainer = DPOTrainer(model, args=config, train_dataset=pref_data, processing_class=tokenizer)",
        "Step 4 (GRPO): def reward_fn(completions, **kwargs): ...; trainer = GRPOTrainer(model, reward_funcs=reward_fn, args=config, train_dataset=dataset)",
        "Step 5 (Reward Model): model = AutoModelForSequenceClassification.from_pretrained(base, num_labels=1); trainer = RewardTrainer(model, args=config, train_dataset=dataset)",
        "Step 6: trainer.train(); trainer.save_model()",
    ]
)

---

skill_manage(
    action="add",
    name="unsloth",
    description="Fast LLM fine-tuning with Unsloth — 2-5x faster training and 50-80% less VRAM. Supports LoRA/QLoRA for Llama, Mistral, Gemma, Qwen and more. Use when memory or speed is a constraint.",
    triggers=["unsloth", "fast fine-tuning", "memory efficient training", "unsloth lora", "2x faster training"],
    steps=[
        "Step 1: Install — pip install unsloth",
        "Step 2: Load model with Unsloth — model, tokenizer = FastLanguageModel.from_pretrained('unsloth/llama-3-8b', load_in_4bit=True)",
        "Step 3: Add LoRA — model = FastLanguageModel.get_peft_model(model, r=16, target_modules=['q_proj','v_proj'])",
        "Step 4: Configure training — trainer = SFTTrainer(model, args=SFTConfig(...))",
        "Step 5: Train — trainer.train()",
        "Step 6: Save — model.save_pretrained('lora_model')",
        "Step 7: Merge and export — model.save_pretrained_merged('merged_model', tokenizer)",
    ]
)

---

## NOTE-TAKING

skill_manage(
    action="add",
    name="obsidian",
    description="Read, create, search, and append to notes in an Obsidian vault. Uses filesystem operations via bash. Vault location set via OBSIDIAN_VAULT_PATH env var.",
    triggers=["obsidian", "obsidian note", "vault note", "markdown note", "create note obsidian", "search obsidian", "wikilink"],
    steps=[
        "Step 1: Set vault path — VAULT=\"${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}\"",
        "Step 2: List all notes — find \"$VAULT\" -name '*.md' -type f",
        "Step 3: Read note — cat \"$VAULT/Note Name.md\"",
        "Step 4: Search by content — grep -rli 'keyword' \"$VAULT\" --include='*.md'",
        "Step 5: Create note — cat > \"$VAULT/New Note.md\" << 'EOF' ... EOF",
        "Step 6: Append — echo 'New content' >> \"$VAULT/Existing Note.md\"",
    ]
)

---

## PRODUCTIVITY

skill_manage(
    action="add",
    name="google-workspace",
    description="Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration via Hermes-managed OAuth2. Prefers gws CLI when available. Use for email, calendar, or document management with Google services.",
    triggers=["gmail", "google calendar", "google drive", "google sheets", "google docs", "google workspace", "send gmail", "read email google"],
    steps=[
        "Step 1: Check auth — python setup.py --check",
        "Step 2 (first time): Create OAuth client at console.cloud.google.com, download JSON",
        "Step 3: Setup — python setup.py --client-secret /path/to/secret.json",
        "Step 4: Get auth URL — python setup.py --auth-url --services all",
        "Step 5: Complete auth — python setup.py --auth-code 'CODE_OR_URL'",
        "Step 6 (Gmail): python google_api.py gmail search 'is:unread' --max 10",
        "Step 7 (Calendar): python google_api.py calendar list",
        "NOTE: Never send email or create events without user confirmation",
    ]
)

---

skill_manage(
    action="add",
    name="linear",
    description="Manage Linear issues, projects, and teams via GraphQL API using curl. Create, update, search, and organize issues. API key auth — no OAuth needed. Use for Linear project management.",
    triggers=["linear", "linear issue", "linear project", "linear app", "create linear issue", "linear task", "engineering issues"],
    steps=[
        "Step 1: Set API key — export LINEAR_API_KEY=your_key",
        "Step 2: List teams — curl -X POST https://api.linear.app/graphql -H 'Authorization: $LINEAR_API_KEY' -d '{\"query\": \"{ teams { nodes { id name key } } }\"}'",
        "Step 3: List issues — query issues(first: 20) with identifier, title, state, assignee",
        "Step 4: Create issue — mutation issueCreate with teamId, title, description, priority",
        "Step 5: Update status — get workflow state UUID, then mutation issueUpdate with stateId",
        "Step 6: Add comment — mutation commentCreate with issueId and body",
    ]
)

---

skill_manage(
    action="add",
    name="maps",
    description="Location intelligence: geocode places, find nearby POIs (44 categories), routing, directions, timezone lookup, and bounding box search. Uses OSM/Nominatim/OSRM. Free, no API key needed.",
    triggers=["find nearby", "directions", "distance", "navigate", "geocode", "maps", "restaurants near", "location search", "how far", "turn by turn"],
    steps=[
        "Step 1: Set script path — MAPS=~/.hermes/skills/maps/scripts/maps_client.py",
        "Step 2 (geocode): python3 $MAPS search 'Eiffel Tower'",
        "Step 3 (nearby): python3 $MAPS nearby --near 'Times Square' --category restaurant --limit 10",
        "Step 4 (distance): python3 $MAPS distance 'Paris' --to 'Lyon' --mode driving",
        "Step 5 (directions): python3 $MAPS directions 'Origin' --to 'Destination' --mode walking",
        "Step 6 (timezone): python3 $MAPS timezone 48.8584 2.2945",
        "Step 7: For Telegram location pins — extract lat/lon, use: python3 $MAPS nearby LAT LON restaurant",
    ]
)

---

skill_manage(
    action="add",
    name="nano-pdf",
    description="Edit PDFs with natural-language instructions using the nano-pdf CLI. Modify text, fix typos, update titles on specific pages. Use when the user needs to make content changes to a PDF.",
    triggers=["edit pdf", "modify pdf", "pdf edit", "fix pdf", "nano-pdf", "change pdf text", "update pdf"],
    steps=[
        "Step 1: Install — uv pip install nano-pdf (or pip install nano-pdf)",
        "Step 2: Edit a page — nano-pdf edit document.pdf PAGE_NUMBER 'instruction'",
        "Step 3 (example): nano-pdf edit deck.pdf 1 'Change the title to Q3 Results'",
        "Step 4: Verify output — check file size and open the PDF",
        "Step 5: If wrong page hit, retry with PAGE ±1 (may be 0-based or 1-based)",
    ]
)

---

skill_manage(
    action="add",
    name="notion",
    description="Create, read, update Notion pages and databases via the Notion API using curl. Search workspaces, manage properties, add content blocks. Requires NOTION_API_KEY.",
    triggers=["notion", "notion page", "notion database", "notion api", "create notion", "update notion", "notion workspace"],
    steps=[
        "Step 1: Set API key — export NOTION_API_KEY=ntn_your_key",
        "Step 2: Share pages with integration in Notion UI",
        "Step 3: Search — curl -X POST https://api.notion.com/v1/search -H 'Authorization: Bearer $NOTION_API_KEY' -H 'Notion-Version: 2025-09-03' -d '{\"query\":\"page title\"}'",
        "Step 4: Get page content — GET /v1/blocks/{page_id}/children",
        "Step 5: Create page — POST /v1/pages with parent and properties",
        "Step 6: Update page — PATCH /v1/pages/{page_id} with properties changes",
        "Step 7: Query database — POST /v1/data_sources/{data_source_id}/query",
    ]
)

---

skill_manage(
    action="add",
    name="ocr-and-documents",
    description="Extract text from PDFs and scanned documents. Decision tree: web_extract for URLs, pymupdf for text-based PDFs, marker-pdf for OCR/scanned/complex layouts. Also handles DOCX and merging.",
    triggers=["extract pdf", "read pdf", "ocr", "pdf text", "scan document", "extract text", "pdf to text", "arxiv paper", "document extraction"],
    steps=[
        "Step 1: Remote URL? — web_extract(urls=['https://arxiv.org/pdf/ID']) — try this first",
        "Step 2: Text-based local PDF? — pip install pymupdf; python3 -c \"import pymupdf; print(pymupdf.open('doc.pdf')[0].get_text())\"",
        "Step 3: Scanned/complex PDF? — pip install marker-pdf; marker_single document.pdf --output_dir ./out",
        "Step 4: DOCX? — pip install python-docx; from docx import Document; doc = Document('file.docx')",
        "Step 5: Merge PDFs — import pymupdf; result = pymupdf.open(); [result.insert_pdf(pymupdf.open(p)) for p in paths]; result.save('merged.pdf')",
    ]
)

---

skill_manage(
    action="add",
    name="powerpoint",
    description="Create, edit, read, and analyze PowerPoint presentations (.pptx). Supports template editing, from-scratch creation with pptxgenjs, visual QA with subagents, and text extraction. Trigger for any .pptx operation.",
    triggers=["powerpoint", "pptx", "slides", "presentation", "deck", "slide deck", "create slides", "edit presentation"],
    steps=[
        "Step 1: Read content — python -m markitdown presentation.pptx",
        "Step 2: Visual overview — python scripts/thumbnail.py presentation.pptx",
        "Step 3 (edit): Unpack — python scripts/office/unpack.py presentation.pptx unpacked/",
        "Step 4 (edit): Modify XML/content in unpacked directory",
        "Step 5 (edit): Repack — python scripts/office/pack.py unpacked/ output.pptx",
        "Step 6 (create from scratch): Use pptxgenjs — npm install -g pptxgenjs",
        "Step 7 (QA): Convert to images — pdftoppm -jpeg -r 150 output.pdf slide; review with subagent",
    ]
)

---

## RED-TEAMING

skill_manage(
    action="add",
    name="godmode",
    description="Jailbreak API-served LLMs using G0DM0D3 techniques: GODMODE CLASSIC system prompts, PARSELTONGUE input obfuscation (33 techniques), and ULTRAPLINIAN multi-model racing. Prompt/API-level — works on closed-source models.",
    triggers=["jailbreak", "godmode", "bypass safety", "parseltongue", "red-team model", "uncensor api", "llm bypass", "g0dm0d3"],
    steps=[
        "Step 1 (auto): Load and run auto_jailbreak() via load_godmode.py",
        "Step 2 (GODMODE CLASSIC): Set jailbreak system prompt in ~/.hermes/config.yaml under agent.system_prompt",
        "Step 3 (prefill): Create ~/.hermes/prefill.json with compliant assistant turn; set agent.prefill_messages_file in config",
        "Step 4 (PARSELTONGUE): python3 parseltongue.py 'query' --tier standard — obfuscates trigger words",
        "Step 5 (ULTRAPLINIAN): race_models(query='...', tier='standard', api_key=OPENROUTER_KEY) — races 24 models, picks least censored",
        "Step 6: Escalate encoding — plain → leetspeak → bubble → braille → morse",
    ]
)

---

## RESEARCH

skill_manage(
    action="add",
    name="arxiv",
    description="Search and retrieve academic papers from arXiv and Semantic Scholar. No API key needed. Full workflow: search, assess impact (citations), read abstracts/PDFs, find related work, generate BibTeX.",
    triggers=["arxiv", "research paper", "academic paper", "find paper", "paper search", "citation", "semantic scholar", "bibtex"],
    steps=[
        "Step 1: Search — curl -s 'https://export.arxiv.org/api/query?search_query=all:TOPIC&max_results=5' | python3 (parse XML)",
        "Step 2: Faster search — python scripts/search_arxiv.py 'topic' --max 10 --sort date",
        "Step 3: Read abstract — web_extract(urls=['https://arxiv.org/abs/ID'])",
        "Step 4: Read full paper — web_extract(urls=['https://arxiv.org/pdf/ID'])",
        "Step 5: Get citation count — curl 'https://api.semanticscholar.org/graph/v1/paper/arXiv:ID?fields=citationCount'",
        "Step 6: Find related — GET /graph/v1/paper/arXiv:ID/references",
        "Step 7: Generate BibTeX — python scripts/search_arxiv.py --id ID (outputs @article entry)",
    ]
)

---

skill_manage(
    action="add",
    name="llm-wiki",
    description="Build and maintain a persistent, interlinked markdown knowledge base (Karpathy's LLM Wiki pattern). Ingest sources, query compiled knowledge, lint for consistency. Use when the user wants a growing research knowledge base.",
    triggers=["wiki", "knowledge base", "llm wiki", "ingest source", "build wiki", "research wiki", "knowledge notes"],
    steps=[
        "Step 1 (new wiki): Create directory structure — raw/, entities/, concepts/, comparisons/, queries/",
        "Step 2 (new wiki): Write SCHEMA.md (domain, conventions, tag taxonomy)",
        "Step 3 (each session): Orient — read SCHEMA.md, index.md, last 30 lines of log.md",
        "Step 4 (ingest): Save raw source → discuss takeaways → check existing pages → write/update wiki pages",
        "Step 5 (ingest): Add wikilinks, update index.md, append to log.md",
        "Step 6 (query): Read index.md → read relevant pages → synthesize answer → file if valuable",
        "Step 7 (lint): Find orphan pages, broken links, stale content, frontmatter errors",
    ]
)

---

skill_manage(
    action="add",
    name="blogwatcher",
    description="Monitor blogs and RSS/Atom feeds for updates using blogwatcher-cli. Add blogs, scan for new articles, track read/unread status, filter by category, import OPML. Use to follow tech blogs.",
    triggers=["rss", "blog feed", "follow blog", "blogwatcher", "news feed", "atom feed", "monitor blog", "read rss"],
    steps=[
        "Step 1: Install — go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest",
        "Step 2: Add blog — blogwatcher-cli add 'Blog Name' https://example.com",
        "Step 3: Scan for new posts — blogwatcher-cli scan",
        "Step 4: List unread — blogwatcher-cli articles",
        "Step 5: Mark as read — blogwatcher-cli read ARTICLE_ID",
        "Step 6: Filter by category — blogwatcher-cli articles --category Engineering",
        "Step 7: Import OPML — blogwatcher-cli import subscriptions.opml",
    ]
)

---

skill_manage(
    action="add",
    name="polymarket",
    description="Query Polymarket prediction market data — search markets, get prices (as probabilities), orderbooks, and price history. Read-only, no authentication needed. Use when asking about event odds or prediction markets.",
    triggers=["polymarket", "prediction market", "market odds", "event probability", "betting odds", "what are the odds", "prediction market price"],
    steps=[
        "Step 1: Search markets — GET https://gamma-api.polymarket.com/events?search=TOPIC",
        "Step 2: Parse response — extract events and their nested markets",
        "Step 3: Read prices — outcomePrices field is JSON-encoded array e.g. ['0.65','0.35'] = 65%/35%",
        "Step 4: Get orderbook — GET https://clob.polymarket.com/book?token_id=TOKEN_ID (from clobTokenIds)",
        "Step 5: Price history — GET https://clob.polymarket.com/prices-history?market=CONDITION_ID",
        "Step 6: Present as — 'Will X happen? — 65.2% Yes ($1.2M volume)'",
    ]
)

---

skill_manage(
    action="add",
    name="research-paper-writing",
    description="End-to-end pipeline for writing ML/AI research papers targeting NeurIPS, ICML, ICLR, ACL, AAAI, and COLM. Covers experiment design, monitoring, statistical analysis, drafting, self-review, and submission.",
    triggers=["write paper", "research paper", "ml paper", "neurips", "icml", "iclr", "acl paper", "academic writing", "paper submission", "conference paper"],
    steps=[
        "Step 1 (setup): Create project structure — src/, experiments/, paper/, results/, scripts/",
        "Step 2 (literature): Search related work via arxiv + semantic scholar; build related_work.md",
        "Step 3 (experiments): Design experiments per claim; implement and run with WandB logging",
        "Step 4 (analysis): Statistical significance tests; generate publication-quality figures",
        "Step 5 (draft): Write paper in LaTeX — Abstract, Intro, Related Work, Method, Experiments, Conclusion",
        "Step 6 (self-review): Check contribution clarity, citation accuracy, experiment-claim alignment",
        "Step 7 (submission): Format for target venue, verify page limits, submit",
        "NOTE: Never hallucinate citations — always fetch programmatically",
    ]
)

---

## SMART HOME

skill_manage(
    action="add",
    name="openhue",
    description="Control Philips Hue lights, rooms, and scenes via the OpenHue CLI. Turn on/off, adjust brightness, color, color temperature, and activate scenes. Requires Hue Bridge on same network.",
    triggers=["hue", "lights", "turn on lights", "dim lights", "philips hue", "openhue", "bedroom lights", "smart lights", "light scene"],
    steps=[
        "Step 1: List lights — openhue get light",
        "Step 2: List rooms — openhue get room",
        "Step 3: List scenes — openhue get scene",
        "Step 4: Control light — openhue set light 'Lamp Name' --on --brightness 70",
        "Step 5: Control room — openhue set room 'Living Room' --on --brightness 50",
        "Step 6: Set color — openhue set light 'Lamp' --on --color red (or --rgb '#FF5500')",
        "Step 7: Activate scene — openhue set scene 'Relax' --room 'Bedroom'",
    ]
)

---

## SOCIAL MEDIA

skill_manage(
    action="add",
    name="xurl",
    description="Interact with X/Twitter via xurl, the official X API CLI. Post, reply, quote, search, timeline, mentions, likes, reposts, bookmarks, follows, DMs, and media upload. Use for any X/Twitter action.",
    triggers=["twitter", "tweet", "x.com", "xurl", "post tweet", "reply tweet", "search twitter", "follow user", "twitter dm", "x api"],
    steps=[
        "Step 1: Verify auth — xurl auth status && xurl whoami",
        "Step 2: Post — xurl post 'Hello world!'",
        "Step 3: Reply — xurl reply POST_ID 'Great point!'",
        "Step 4: Search — xurl search 'golang' -n 10",
        "Step 5: Like/Repost — xurl like POST_ID / xurl repost POST_ID",
        "Step 6: Follow — xurl follow @handle",
        "Step 7: DM — xurl dm @handle 'message'",
        "SECURITY: Never read ~/.xurl or pass credentials inline; never use --verbose",
    ]
)

---

## SOFTWARE DEVELOPMENT

skill_manage(
    action="add",
    name="plan",
    description="Plan mode for Hermes — inspect context, write a markdown plan into .hermes/plans/ without executing any code. Use when the user wants a plan instead of implementation.",
    triggers=["plan", "write a plan", "plan mode", "create a plan", "don't implement", "just plan", "planning"],
    steps=[
        "Step 1: Inspect repo context with read-only tools (no mutations)",
        "Step 2: Understand requirements and constraints",
        "Step 3: Draft plan with: Goal, Context, Proposed Approach, Step-by-step Plan, Files to Change, Tests, Risks",
        "Step 4: Save plan — write_file('.hermes/plans/YYYY-MM-DD_HHMMSS-slug.md')",
        "Step 5: Report plan path to user",
        "RULE: Do not implement code, edit project files, commit, push, or run mutations",
    ]
)

---

skill_manage(
    action="add",
    name="subagent-driven-development",
    description="Execute implementation plans by dispatching fresh subagents per task with two-stage review (spec compliance then code quality). Use when executing multi-step plans with independent tasks.",
    triggers=["subagent", "delegate tasks", "dispatch subagent", "execute plan", "implement plan", "subagent development", "parallel tasks"],
    steps=[
        "Step 1: Read plan file once; create todo list with all tasks",
        "Step 2 per task: Dispatch implementer subagent via delegate_task() with full context + TDD instructions",
        "Step 3 per task: Dispatch spec compliance reviewer — verify all requirements met (PASS/FAIL)",
        "Step 4 per task: If spec PASS → dispatch code quality reviewer (critical/important/minor issues)",
        "Step 5 per task: If any issues → fix subagent → re-review; repeat until approved",
        "Step 6 per task: Mark complete in todo list",
        "Step 7 (final): Dispatch integration reviewer for full implementation",
    ]
)

---

skill_manage(
    action="add",
    name="requesting-code-review",
    description="Pre-commit verification pipeline: static security scan, baseline-aware quality gates, independent reviewer subagent, and auto-fix loop. Use after code changes and before committing or pushing.",
    triggers=["code review", "verify code", "pre-commit review", "review before commit", "security scan", "verify changes", "check code"],
    steps=[
        "Step 1: Get diff — git diff --cached",
        "Step 2: Static scan — grep for secrets, shell injection, eval/exec, SQL injection, pickle.loads",
        "Step 3: Baseline tests — capture failure count before changes (stash, run, pop); only new failures matter",
        "Step 4: Self-review checklist — no secrets, input validation, parameterized SQL, error handling",
        "Step 5: Independent reviewer — delegate_task() with ONLY the diff; returns JSON {passed, security_concerns, logic_errors, suggestions}",
        "Step 6: If PASS → git add -A && git commit -m '[verified] description'",
        "Step 7: If FAIL → auto-fix loop (max 2 cycles); escalate to user if still failing after 2",
    ]
)

---

skill_manage(
    action="add",
    name="systematic-debugging",
    description="4-phase root cause debugging — NO fixes without understanding the problem first. Use for any bug, test failure, or unexpected behavior. Systematic approach: reproduce, trace, hypothesize, fix.",
    triggers=["debug", "fix bug", "test failure", "unexpected behavior", "debugging", "bug investigation", "root cause"],
    steps=[
        "Phase 1 (Root Cause): Read error messages fully; reproduce consistently; check recent git changes; trace data flow to source",
        "Phase 2 (Pattern): Find working similar code; compare differences; understand dependencies",
        "Phase 3 (Hypothesis): Form single clear hypothesis ('X fails because Y'); test with MINIMAL change; one variable at a time",
        "Phase 4 (Fix): Write failing regression test first; fix root cause (not symptom); verify test passes; run full suite",
        "RULE: No fixes without Phase 1 complete",
        "RULE: If 3+ fixes failed → question architecture, discuss with user before trying more fixes",
    ]
)

---

skill_manage(
    action="add",
    name="test-driven-development",
    description="Enforces RED-GREEN-REFACTOR TDD cycle. Write failing test first, watch it fail, write minimal code to pass, refactor. Use before writing any implementation code.",
    triggers=["tdd", "test driven", "write tests", "test first", "red green refactor", "failing test", "unit test"],
    steps=[
        "RED: Write one minimal failing test with clear descriptive name; test one behavior",
        "Verify RED: Run test — must FAIL for expected reason (feature missing, not syntax error)",
        "GREEN: Write SIMPLEST code to pass the test — hardcoding OK, no extras",
        "Verify GREEN: Run specific test (PASS); run full suite (no regressions)",
        "REFACTOR: Remove duplication, improve names — tests must stay green throughout",
        "Repeat: Write next failing test for next behavior",
        "IRON LAW: No production code without a failing test first. Delete code written before tests and restart.",
    ]
)

---

skill_manage(
    action="add",
    name="writing-plans",
    description="Create comprehensive implementation plans with bite-sized tasks, exact file paths, and complete code examples. Assumes implementer has zero context. Use before multi-step feature implementation.",
    triggers=["write plan", "create plan", "implementation plan", "plan feature", "break down task", "task plan", "spec to plan"],
    steps=[
        "Step 1: Understand requirements — read spec, design docs, acceptance criteria",
        "Step 2: Explore codebase — find similar features, check existing tests, read key files",
        "Step 3: Design approach — architecture pattern, file organization, dependencies",
        "Step 4: Write tasks (bite-sized, 2-5 min each) — Setup → Core → Edge Cases → Integration → Cleanup",
        "Step 5: Per task: exact file paths + complete code + exact commands + expected output + verification steps",
        "Step 6: Review — tasks sequential? paths exact? code copy-pasteable? DRY/YAGNI/TDD applied?",
        "Step 7: Save to docs/plans/YYYY-MM-DD-feature-name.md; offer to execute with subagent-driven-development",
    ]
)

---
# END OF EXPORT
# Total skills: 71
# Categories: Apple(4), Autonomous AI Agents(4), Creative(11), Data Science(1),
#   Devops(1), Dogfood(1), Email(1), Gaming(2), GitHub(6), MCP(1), Media(4),
#   MLOps-Evaluation(2), MLOps-Hub(1), MLOps-Inference(4), MLOps-Models(2),
#   MLOps-Research(1), MLOps-Training(3), Note-Taking(1), Productivity(7),
#   Red-Teaming(1), Research(5), Smart-Home(1), Social-Media(1), Software-Dev(6)
