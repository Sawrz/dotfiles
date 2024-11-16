#!/bin/sh

# Setting this, so the repo does not need to be given on the commandline:
export BORG_REPO=/net/backups/games/

# See the section "Passphrase notes" for more infos.
export BORG_PASSPHRASE=$(cat ~/.secrets/blastoise-games-backup.secret)

# some helpers and error handling:
info() { printf "\n%s %s\n\n" "$( date )" "$*" >&2; }
trap 'echo $( date ) Backup interrupted >&2; exit 2' INT TERM

info "Starting backup"

# Backup the most important directories into an archive named after
# the machine this script is currently running on:

borg create                                                                                                                                     \
    --verbose                                                                                                                                   \
    --filter AME                                                                                                                                \
    --list                                                                                                                                      \
    --stats                                                                                                                                     \
    --show-rc                                                                                                                                   \
    --compression lz4                                                                                                                           \
    --exclude-caches                                                                                                                            \
    --exclude '/home/*/.cache/*'                                                                                                                \
    --exclude '/var/cache/*'                                                                                                                    \
    --exclude '/var/tmp/*'                                                                                                                      \
                                                                                                                                                \
    ::'{hostname}-{now}'                                                                                                                        \
    /mnt/games/SteamLibrary/steamapps/common/Kenshi/save                                                                                        \
    /mnt/games/SteamLibrary/steamapps/common/Kenshi/data/mods.cfg                                                                               \
    /home/sandro/.local/share/Steam/steamapps/compatdata/233860/pfx/drive_c/users/steamuser/Local\ Settings/Application\ Data/kenshi            \
    /home/sandro/.config/unity3d/Ludeon\ Studios/RimWorld\ by\ Ludeon\ Studios/Config                                                           \
    /home/sandro/.config/unity3d/Ludeon\ Studios/RimWorld\ by\ Ludeon\ Studios/ModLists                                                         \
    /mnt/games/SteamLibrary/steamapps/common/Software\ Inc/Saves                                                                                \
    /home/sandro/.config/unity3d/Ludeon\ Studios/RimWorld\ by\ Ludeon\ Studios                                                                  \
    /mnt/games/Lutris/origin/drive_c/users/sandro/My\ Documents/Electronic\ Arts/The\ Sims\ 4/                                                  \

backup_exit=$?

info "Pruning repository"

# Use the `prune` subcommand to maintain 7 daily, 4 weekly and 6 monthly
# archives of THIS machine. The '{hostname}-' prefix is very important to
# limit prune's operation to this machine's archives and not apply to
# other machines' archives also:

borg prune                          \
    --list                          \
    --prefix '{hostname}-'          \
    --show-rc                       \
    --keep-daily    7               \
    --keep-weekly   4               \
    --keep-monthly  6               \

prune_exit=$?

# use highest exit code as global exit code
global_exit=$(( backup_exit > prune_exit ? backup_exit : prune_exit ))

if [ ${global_exit} -eq 0 ]; then
    msg="Backup and Prune finished successfully"
    urgency=0
elif [ ${global_exit} -eq 1 ]; then
    msg="Backup and/or Prune finished with warnings"
    urgency=1
else
    msg="Backup and/or Prune finished with errors"
    urgency=2
fi

info $msg
dunstify -a 'Games Backup' -u $urgency "${msg}"

exit ${global_exit}
