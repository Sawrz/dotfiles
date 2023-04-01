# dotfiles

This repository contains my dotfiles configuration. I use it with MacOS; however, it might also work on Linux. 

## Requirements
[stow](https://www.gnu.org/software/stow/) creates symlinks in your home folder. That results in having your active config files live in this repository locally. Install `stow` with [Homebrew](https://brew.sh) with the following command:

``` zsh
brew install stow
```

## Usage

With `stow` you choose which configs to enable. For example, to set up the configs for Alacritty, enter the following into your console while being in the root of this repository:

```zsh
stow alacritty
```

However, remember that you can create symlinks only if no file with the same name exists. Therefore, you must delete your `.zshrc` and `.zprofile` to enable my `zsh` config.