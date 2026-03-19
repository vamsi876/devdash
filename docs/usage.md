# Usage Guide

## Launching GadgetBox

Once installed, start the app:

```bash
gadgetbox
```

A wrench icon (🔧) appears in your system tray. Click it to open the menu.

## Accessing Tools

From the GadgetBox menu, tools are organized by category:

- **Formatters** — JSON Formatter
- **Decoders** — JWT Decoder, Base64, URL Decode
- **Generators** — UUID / ULID, Password, Lorem Ipsum
- **Encoders** — Base64, URL Encode, Hash Generator
- **Converters** — Timestamp Converter, Color Converter
- **Utilities** — Regex Tester, Cron Parser

Click any tool to open its dialog. Enter your input and see results instantly.

## Smart Clipboard Auto-Detection

The "Clipboard: Auto-detect" feature intelligently identifies what's in your clipboard and opens the right tool.

### How to Use It

1. Copy something to your clipboard (any format)
2. Click **Clipboard: Auto-detect** in the GadgetBox menu
3. The matching tool opens with your content pre-filled

### Supported Formats

- **JSON** — Objects or arrays
- **JWT** — Tokens starting with `eyJ...`
- **UUID** — Standard UUID format
- **Base64** — Encoded text (must be valid length)
- **Unix Timestamps** — 10-digit (seconds) or 13-digit (milliseconds)
- **URLs** — Starting with `http://` or `https://`
- **URL-Encoded** — Text with `%XX` patterns
- **Hex Colors** — `#FFF`, `#FFFFFF`
- **Cron Expressions** — 5-6 space-separated fields

### Examples

```
Clipboard Content → Tool Opens
{"name":"John"}  → JSON Formatter
eyJhbGc... → JWT Decoder
f47ac10b-58cc-4372-a567-0e02b2c3d479 → UUID / ULID Generator
aGVsbG8gd29ybGQ= → Base64 Decode
1234567890 → Timestamp Converter
https://example.com/path?a=1&b=2 → URL Decode
#FF5733 → Color Converter
0 0 * * * → Cron Parser
```

If no match is found, you'll see a notification but can manually select a tool.

## Individual Tools

### JSON Formatter

Format, validate, or minify JSON.

**Input:** Any JSON string (object, array, or primitive)

**Modes:**
- **Format** — Pretty-print with 2-space indentation
- **Minify** — Remove all whitespace
- **Validate** — Check if JSON is valid (no output if valid)

**Examples:**

```
Input: {"name":"John","age":30}
Output (Format):
{
  "name": "John",
  "age": 30
}

Output (Minify): {"name":"John","age":30}
```

### JWT Decoder

Decode and inspect JSON Web Tokens.

**Input:** JWT token (three Base64-encoded parts separated by dots)

**Output:**
- Header (algorithm and type)
- Payload (claims and data)
- Signature validity (can't verify without secret)

**Example:**

```
Input: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U

Output:
Header: {"alg":"HS256","typ":"JWT"}
Payload: {"sub":"1234567890","name":"John Doe"}
Signature: Valid Base64 (secret verification not possible without key)
```

### UUID / ULID Generator

Generate and validate UUID and ULID identifiers.

**Input (Optional):** UUID to validate, or leave blank to generate

**Options:**
- **Version** — v4 (random), v7 (timestamp), ulid
- **Count** — Generate multiple (1-100)
- **Uppercase** — Output as uppercase

**Examples:**

```
Generate UUID v4:
f47ac10b-58cc-4372-a567-0e02b2c3d479

Generate UUID v7 (timestamp-based):
0190c6c7-c7e5-7dcc-aaa3-a2f7f1b5c5d2

Generate ULID:
01ARZ3NDEKTSV4RRFFQ69G5FAV

Validate UUID:
Input: f47ac10b-58cc-4372-a567-0e02b2c3d479
Output: Valid UUID (version 4): f47ac10b-58cc-4372-a567-0e02b2c3d479
```

### Base64 Encode/Decode

Convert between text and Base64.

**Input:** Text to encode or Base64 string to decode

**Output:** Encoded or decoded result

**Examples:**

```
Encode:
Input: Hello, World!
Output: SGVsbG8sIFdvcmxkIQ==

Decode:
Input: SGVsbG8sIFdvcmxkIQ==
Output: Hello, World!
```

### Hash Generator

Generate hashes using various algorithms.

**Input:** Text to hash

**Options:**
- **Algorithm** — MD5, SHA256, SHA512
- Default is configurable in config.yaml

**Examples:**

```
SHA256 of "password":
5e884898da28047151d0e56f8dc629d9:3dde512d4e1fa2e6b2a05f5e7d5f6f5

MD5 of "Hello":
8b1a9953c4611296aaf7a3c4ab6f3c97
```

### Timestamp Converter

Convert between Unix timestamps and human-readable dates.

**Input:** Unix timestamp (10 or 13 digits) or blank to get current time

**Output:** Readable date and time

**Format:** Configurable in config.yaml (default: `%Y-%m-%d %H:%M:%S`)

**Examples:**

```
Input: 1609459200
Output: 2021-01-01 00:00:00

Input: 1609459200000 (milliseconds)
Output: 2021-01-01 00:00:00

Leave blank to convert current time
Output: 2024-01-15 14:30:45
```

### URL Encode/Decode

Encode text for URLs or decode URL-safe strings.

**Input:** Plain text to encode or encoded string to decode

**Output:** Encoded or decoded result

**Examples:**

```
Encode:
Input: hello world & special chars
Output: hello%20world%20%26%20special%20chars

Decode:
Input: hello%20world
Output: hello world
```

### Regex Tester

Test regular expressions with live matching.

**Input:** Text to match against

**Options:**
- **Pattern** — Regular expression
- **Flags** — Case-insensitive, multiline, etc.

**Output:** All matches highlighted

**Examples:**

```
Pattern: \d{3}-\d{3}-\d{4}
Input: Call me at 555-123-4567
Output: 555-123-4567 (Match found)

Pattern: \b\w{5}\b
Input: The quick brown fox
Output: quick, brown (2 matches)
```

### Color Converter

Convert between color formats.

**Input:** Hex (#FFF, #FFFFFF), RGB (r, g, b), or HSL

**Output:** All format conversions

**Examples:**

```
Input: #FF5733
Output:
  RGB: rgb(255, 87, 51)
  HSL: hsl(9, 100%, 60%)
  Hex: #FF5733

Input: rgb(255, 87, 51)
Output: (converted to hex and HSL)
```

### Lorem Ipsum Generator

Generate placeholder text.

**Input:** Number of paragraphs or words

**Output:** Lorem ipsum text

**Examples:**

```
Generate 3 paragraphs:
Lorem ipsum dolor sit amet, consectetur adipiscing elit...
[paragraph 2]
[paragraph 3]

Generate 50 words:
Lorem ipsum dolor sit amet... (50 words)
```

### Password Generator

Create secure random passwords.

**Input:** (Optional) Leave blank for default

**Options:**
- **Length** — Number of characters (default in config: 16)
- **Include Symbols** — Add special characters
- **Include Numbers** — Add digits

**Examples:**

```
Generate with defaults:
aB7xK#mN9@pQr2Yz

Generate 32 characters:
aB7xK#mN9@pQr2YzL5qW8tU1vS3dFgH6
```

### Cron Parser

Parse and explain cron expressions.

**Input:** Cron expression (5 or 6 fields)

**Output:** Human-readable schedule description

**Examples:**

```
Input: 0 0 * * *
Output: Every day at 00:00 (midnight)

Input: 0 9 * * MON-FRI
Output: Every weekday at 09:00

Input: */15 * * * *
Output: Every 15 minutes

Input: 0 0 1 * *
Output: First day of every month at 00:00
```

## Configuration

GadgetBox stores preferences in `~/.config/gadgetbox/config.yaml` on macOS/Linux, or `%APPDATA%/gadgetbox/config.yaml` on Windows. Create or edit this file to customize behavior.

**Available Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `default_hash_algorithm` | string | `sha256` | Hash algorithm: `md5`, `sha256`, `sha512` |
| `timestamp_format` | string | `%Y-%m-%d %H:%M:%S` | Python strftime format for date display |
| `password_length` | integer | `16` | Default password length (1-128) |
| `uuid_version` | string | `v4` | UUID version: `v4` or `v7` |
| `auto_clipboard_detection` | boolean | `true` | Enable auto-detect feature |
| `clipboard_watcher` | boolean | `false` | Watch clipboard continuously (experimental) |

**Example Configuration:**

```yaml
# Use SHA512 for hashes
default_hash_algorithm: sha512

# Verbose timestamp format
timestamp_format: "%A, %B %d, %Y at %I:%M %p"

# Longer passwords
password_length: 32

# Prefer UUID v7 (timestamp-sortable)
uuid_version: v7

# Keep auto-detection enabled
auto_clipboard_detection: true

# Disable experimental clipboard watcher
clipboard_watcher: false
```

## Tips & Tricks

### Copy to Clipboard Automatically

After getting a result, you can copy it to your clipboard with Cmd+C (standard macOS copy).

### Chain Tools Together

Use auto-detect to quickly chain operations:
1. Format JSON, copy result
2. Use auto-detect to encode to Base64
3. Use auto-detect to hash the Base64

### Use Case Examples

**Debug JWT tokens from logs:**
- Copy the token from your logs
- Click "Clipboard: Auto-detect" → JWT Decoder opens
- Inspect the payload

**Convert API timestamps:**
- Copy the timestamp from API response
- Click "Clipboard: Auto-detect" → Timestamp Converter opens
- See the human-readable date

**Generate UUIDs for database seeding:**
- Generate multiple UUIDs (set count to 10)
- Copy all at once
- Paste into your SQL script

## Keyboard Shortcuts

GadgetBox respects standard keyboard shortcuts across platforms:

- **Ctrl+W** / **Cmd+W** — Close current tool dialog
- **Ctrl+Q** / **Cmd+Q** — Quit GadgetBox
- **Ctrl+C** / **Cmd+C** — Copy result to clipboard

## Quitting GadgetBox

To quit the app:

1. Click the GadgetBox icon in the system tray
2. Select "Quit"

Or press the standard quit shortcut (Cmd+Q on macOS, Ctrl+Q on Windows/Linux).

The app won't run in the background. Relaunch with `gadgetbox` when needed.
