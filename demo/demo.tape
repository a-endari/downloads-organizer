Output demo/demo.gif

Set Shell zsh
Set Theme "Catppuccin Mocha"
Set Width 1200
Set Height 750
Set WindowBar Colorful
Set WindowBarSize 42
Set BorderRadius 12
Set FontFamily "MesloLGS NF"
Set FontSize 19
Set LineHeight 1.35
Set TypingSpeed 75ms
Set Framerate 30
Set CursorBlink true

# ─────────────────────────────────────────────
# Prepare the demo
# ─────────────────────────────────────────────

Hide

# Load the shell configuration and initialize the environment invisibly
Type "source ~/.zshrc"
Enter 1

Type "rm -rf ~/Downloads/Demo && mkdir -p ~/Downloads/Demo/Archives"
Enter 1

Type "touch ~/Downloads/Demo/{report.pdf,presentation.pptx,budget.xlsx,invoice_2026.pdf,invoice_final.pdf,invoice_final_final.pdf,tax_form_scanned.PDF,receipt_1847.pdf,photo.jpg,vacation.jpg,vacation_raw.CR2,screenshot.png,screenshot_2026-09-25.png,logo.svg,banner.ai,banner_v2.ai,archive.zip,backup.tar.gz,config.bak,script.py,app.js,data.json,payload.xml,notes.txt,todo_list.md,meeting_notes.txt,installer.dmg,setup_v1.2.pkg,update.pkg,random_file.tmp,project_backup.zip}"
Enter 1

Type "touch ~/Downloads/Demo/Archives/{project_backup.zip}"
Enter 1

# Enter the project directory
Type "cd /Users/abbas/Dropbox/MyProjects/downloads-organizer"
Enter 1
Sleep 700ms

Type "source .venv/bin/activate"
Enter 1
Sleep 1s

Type "clear"
Enter 1
Sleep 500ms

Show

# ─────────────────────────────────────────────
# BEFORE
# ─────────────────────────────────────────────

Type "# Let's take a look at a messy demo folder first"
Enter 1
Sleep 1s
Type "lsd ~/Downloads/Demo"
Enter 1
Sleep 2s

# Scroll through the tree if it exceeds the viewport
ScrollUp@100ms 8
Sleep 1s
ScrollDown@100ms 8
Sleep 3s

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

Type "downloads-organizer --help"
Enter 1
Sleep 2s

# Show the beginning of the long result, then scroll through it
ScrollUp@100ms 8
Sleep 1s
ScrollDown@100ms 8
Sleep 3s

# ─────────────────────────────────────────────
# DRY RUN
# ─────────────────────────────────────────────

# Hide
# Type "clear"
# Enter 1
# Sleep 500ms
# Show

# Type "# Let's do a dry run first:"
# Enter 1
# Sleep 1s
# 
# Type "downloads-organizer organize ~/Downloads/Demo --dry-run -v"
# Enter 1
# Sleep 2s

# ScrollUp@100ms 10
# Sleep 1s
# ScrollDown@100ms 10
# Sleep 3s

# ─────────────────────────────────────────────
# ORGANIZE
# ─────────────────────────────────────────────

Type "# You can also use `dlo` or `ae-dlo` as aliases for `downloads-organizer`"
Enter 1
Sleep 1s

Type "dlo organize ~/Downloads/Demo"
Enter 1
Sleep 2s

# ─────────────────────────────────────────────
# AFTER
# ─────────────────────────────────────────────


Type "# Now let's take a look at the final result:"
Enter 1
Sleep 1s
Type "lsd ~/Downloads/Demo"
Enter 1
Sleep 2s
Type "# Are the files organized? let's take a deeper look:"
Enter 1

Type "lsd --tree --depth 2 ~/Downloads/Demo"
Enter 1
Sleep 2s

ScrollUp@150ms 25
Sleep 1.5s
ScrollDown@150ms 25
Sleep 5s
