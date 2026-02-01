[![Tests](https://github.com/esteban03/anxiety/actions/workflows/tests.yml/badge.svg)](https://github.com/esteban03/anxiety/actions/workflows/tests.yml)

> 🚧 **Note:** This project is still under development.

# Hacking my Digital Hoarding, one file at a time

This is a personal project I whipped up to keep my fucking download folder organized for once. It is specifically tailored for my Mac setup and isn't intended for widespread distribution as a polished package. I'm sharing the code in a raw, custom way. If it helps you solve a similar problem or inspires your own automation tools, that's great!

I tend to hoard files, installers, and documents with the false promise that _"they will be useful in the future."_ Surprise: they never are. The result is a massive cognitive load that affects both my productivity and my Mac's storage.

This project is born from my own **"Mental Framework"** to hack digital hoarding:

1. **Identify the trash:** Recognizing single-use files (currently focusing on installers like `.dmg` or `.app`).
2. **Reduce detachment friction:** Instead of deleting them immediately (which triggers that _"what if I need it later?"_ anxiety), I move them to a transition zone.
3. **Automate the habit:** I've realized that the cognitive cost and psychological resistance to deleting things are too high for me. I've accepted it. So, I prefer this script to act as my "organized self" and do the job for me automatically.

<img width="2752" height="1536" alt="fucking-folder" src="https://github.com/user-attachments/assets/6161fb7b-aedf-48b2-8b62-6402e8da4df3" />

## 🚀 The Solution: Version 1.0

This is the first iteration of my cleaning assistant. It uses a **Watchdog** (filesystem observer) to monitor folders in real-time and apply my framework rules.

### How it works:

- **Auto-Detection:** Monitoring configured folders in real-time.
- **Zen Download (Internal: `should-be-deleted`):** Tackles digital hoarding by moving files through a transition zone before deletion.
- **Zen Desktop:** Keeps your Mac desktop pristine by filing away items instantly.
- **Smart Filter:** Files are processed based on the active strategy (Downloads, Desktop, or both).
- **Dual Strategy Support:** Both are active by default, though they can be enabled independently.

## 📋 Strategies & Rules

The project operates under two distinct mental models to maintain digital health:

### 1. Zen Download (Internal: `should-be-deleted`)

Designed to combat the anxiety of "what if I need this later?" and the self-deception that every installer is a treasure.

- **Objective:** Maintain an organized Downloads folder by eliminating accumulated clutter.
- **Movement Rule:** Files must stay in Downloads for at least **24 hours** before moving (the "cooling off" period).
- **Transition Zone:** Files move to `~/Downloads/should-be-deleted/`.
- **Final Purge:** After **1 week** in the transition zone, files are automatically deleted.
- **Rigid Implementation:** This follows strict rules to prevent you from lying to yourself about a file's future utility.

> [!IMPORTANT]
> **macOS Behavior:** Moving files resets the creation timestamp (`st_ctime`). The 1-week grace period starts from the moment the file is moved to the transition zone.

### 2. Zen Desktop

The Mac desktop is beautiful when it's clear. This strategy ensures you always have that "fresh install" feeling.

- **Objective:** Maintain a pristine, zen-like workspace.
- **Action:** Any file arriving on the desktop is **immediately** moved into a subfolder named `Desktop` (`~/Desktop/Desktop`).
- **File-Only Rule:** This strategy **does not move folders**. This allows you to keep specific, hand-picked project folders on your desktop while the "loose" file clutter disappears.
- **Safety:** There is **no deletion** involved in this strategy. It just moves things out of sight until you need them.

### Temporary File Protection

Both strategies skip files matching these patterns to avoid interfering with active tasks:

- `.com.google.Chrome` (Chrome temporary downloads)
- `.tmp`, `.partial`, `.crdownload` (partial downloads)
- `~$` (Office temporary files)

## 🛠️ Technologies

- **Python 3.14+**
- [**uv**](https://github.com/astral-sh/uv): Fast Python package management.
- [**Typer**](https://typer.tiangolo.com/): Powering the CLI interface.
- [**Watchdog**](https://python-watchdog.readthedocs.io/): Real-time filesystem observation.

## 📦 Installation

To install `anxiety` as a global tool using `uv` (recommended):

```bash
uv tool install git+https://github.com/esteban03/anxiety.git
```

This will make the `anxiety` command available anywhere in your terminal.

> [!TIP]
> If you want to contribute or develop, check the [Development Guide](DEVELOPMENT.md).

## 🚀 Usage

By default, **both strategies are active**. You can run `anxiety` as a foreground observer or a background service.

### Available Strategy Flags

- **`--nice_download` / `-s`:** Enables Zen Download.
- **`--nice_desktop` / `-d`:** Enables Zen Desktop.

### Monitor in Foreground

To start watching immediately:

**Watch both (default):**

```bash
anxiety watch
```

**Watch specific strategies:**

```bash
# Only Downloads
anxiety watch -s

# Only Desktop
anxiety watch -d
```

### Background Service (Daemon)

You can run the cleaner as a background service that starts automatically when you log in.

**Start & Enable (both strategies by default):**

```bash
anxiety init
```

**Start with specific strategies:**

```bash
# Only Downloads
anxiety init --nice_download

# Only Desktop
anxiety init --nice_desktop
```

This command automatically:

1. Generates the Launch Agent configuration.
2. Installs it to `~/Library/LaunchAgents/me.steban.www.anxiety.plist`.
3. **Starts the service immediately.**

**Check Status:**

```bash
anxiety status
```

**Stop & Disable:**

```bash
anxiety stop
```

### Logs

To verify the service is working or debug issues, check the logs:

```bash
tail -f /tmp/me.steban.www.anxiety.stdout.log
```

## 🔮 Next Steps

- [x] **Desktop Zen Mode:** Auto-organize the Mac Desktop to keep it always pristine, highlighting the wallpaper and reducing visual noise.
- [x] **Auto-Purge:** Implement auto-deletion rules for the `should-be-deleted` folder (e.g., delete files older than 30 days).
- [ ] **PyPI Publication:** Package `anxiety` for easy installation via `pip install anxiety`.
- [ ] **Homebrew Support:** Create a formula to install via `brew install anxiety`.
