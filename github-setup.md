---
layout: default
title: GitHub Setup
permalink: /github-setup/
---

# Install Git & Create a GitHub Account

This section walks through creating a GitHub account, installing Git locally, and configuring SSH access so you can push/pull repositories securely without repeatedly entering your password.

---

## 1. Create a GitHub account

1. Go to [GitHub](https://github.com/).
2. Click **Sign up**.
3. Follow the prompts to create your account (email, username, password).
4. Verify your email address when prompted.
5. Enable two-factor authentication (2FA) in **Settings → Password and authentication**.

## 2. Install Git locally

Choose the instructions for your system.

### Linux (Ubuntu/Debian)

In a terminal window, run the following command:

```bash
sudo apt update
sudo apt install git
git --version
```

### macOS

Most versions of macOS already have Git installed. Open a terminal window and check to see if Git is already activated. If Git is not installed, you can install the latest version from [GitHub](https://github.com/).

If you have Homebrew already installed, you can use the following command:

```bash
brew install git
git --version
```

### Windows

Install Git for Windows from [https://git-scm.com/install/](https://git-scm.com/install/).

During installation, keep the default options unless you have a reason to change them.

Open Git Bash and verify:

```bash
git --version
```

## 3. Generate an SSH key and add it to GitHub

SSH keys let you authenticate with GitHub securely. More details here: [https://docs.github.com/en/authentication/connecting-to-github-with-ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

### 3.1. Generate a key

Enter the following terminal window, replacing the email address in quotes with the email associated with your GitHub account:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press `Enter` without entering anything to accept the default file location.

Enter a passphrase if you want extra security (recommended). If you do not want a password, press `Enter` to continue without entering anything.

### 3.2. Copy your public key

Enter the following in the same terminal window:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starting with ssh-ed25519).

### 3.3. Add the key to GitHub

1. Go to **GitHub** → **Settings**.
2. Click **SSH and GPG keys**.
3. Click **New SSH key**.
4. Paste your public key into the key field.
5. Enter a descriptive title (e.g., `laptop`, `desktop`, `cluster`).
6. Click **Add SSH key**.

### 3.4. Test the connection

Enter the following in the same terminal window:

```bash
ssh -T git@github.com
```

You should see a message indicating that authentication succeeded.

---

# Git Cheat Sheet

When running G&R simulations, you often need to build on existing code. This guide follows the typical workflow: finding a repository on GitHub, forking it to your account, creating a space on your local machine to experiment with code, and securely pushing your changes back to a new branch on your fork that is accessible by others who want to use your code.

## 1. Get the code

Find the repository of the code you want to use. Hit the **"Fork"** button on the original GitHub repository to create a copy under your own account. Then, clone the repository to your local machine.

* **Clone your forked repository locally:**

In a terminal window, enter the following, replacing `[url]` with the link to the GitHub repository (e.g., `git@github.com:febiosoftware/FEBio.git`).

    ```bash
    git clone [url]
    ```

## 2. Make a new branch

To ensure your experiments don't break the original stable code, you should create a dedicated development branch locally. 

* **List all existing branches:**
    ```bash
    git branch
    ```
* **Create a new development branch:**

Replace `[branch-name]` with the name you want to use for your branch.

    ```bash
    git branch [branch-name]
    ```
* **Switch to your new branch:**
    ```bash
    git checkout [branch-name]
    ```

## 3. Make your changes

On your local machine, edit the code until you are happy with your workflow. Then, tell Git which files you want it to track and update (stage).

* **Check the status of your files:**
    *(Shows modified files in your working directory and what is staged for your next commit.)*
    ```bash
    git status
    ```
* **Stage a specific file:**

Replace `[file]` with the file name(s) you want to update.

    ```bash
    git add [file]
    ```
* **Or, stage ALL your current changes:**
    ```bash
    git add .
    ```
* **Commit your staged changes to your local history:**
    *(Leave a clear note for yourself and future collaborators summarizing what changes you made in plain language.)*

Replace `[message]` with your note.

    ```bash
    git commit -m "[message]"
    ```

## 4. Tell Git where to put your new branch

So far, your changes are only on your local machine. Now, you need to push them up to your new branch on GitHub so other people can see and build on them.

* **Link a remote repository:**
    *(If you need to define where your code is going, or want to link back to the original source you forked from, your default `alias` is `origin`.)*

Replace `[url]` with the link to the remote repository (e.g., `git@github.com:febiosoftware/FEBio.git`).

    ```bash
    git remote add [alias] [url]
    ```
* **Push your local branch up to your GitHub account:**

    ```bash
    git push [alias] [branch-name]
    ```

##  5. Retrieve changes to your branch
If collaborators have updated the code, or you want to sync your local branch with remote updates (what's on your GitHub account):

* **Fetch and merge remote changes into your local workspace:**

    ```bash
    git pull
    ```
