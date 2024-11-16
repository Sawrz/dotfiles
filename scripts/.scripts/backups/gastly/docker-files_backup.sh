#!/bin/sh

# Set Service Directory Path
SERVICE_DIR=/home/sandro/docker-files

# Setting this, so the repo does not need to be given on the command-line:
export BORG_REPO=/mnt/backups/docker-files

# See the section "Passphrase notes" for more info.
export BORG_PASSPHRASE=$(cat /home/sandro/.secrets/docker-files_backup.secret)

# some helpers and error handling:
info() { printf "\n%s %s\n\n" "$( date )" "$*" >&2; }
trap 'echo $( date ) Backup interrupted >&2; exit 2' INT TERM

info "Starting backup."

# Backup the most important directories into an archive named after
# the machine this script is currently running on:

borg create                                                                                          \
    --verbose                                                                                        \
    --filter AME                                                                                     \
    --list                                                                                           \
    --stats                                                                                          \
    --show-rc                                                                                        \
    --compression lz4                                                                                \
    --exclude-caches                                                                                 \
    --exclude '/home/*/.cache/*'                                                                     \
    --exclude '/var/cache/*'                                                                         \
    --exclude '/var/tmp/*'                                                                           \
                                                                                                     \
    ::'{hostname}-{now}'                                                                             \
    $SERVICE_DIR                                                                                     \

backup_exit=$?

info "Pruning repository."

# Use the `prune` subcommand to maintain 7 daily, 4 weekly and 6 monthly
# archives of THIS machine. The '{hostname}-' prefix is very important to
# limit prune's operation to this machine's archives and not apply to
# other machines' archives also:

borg prune                          \
    --list                          \
    --prefix '{hostname}-'          \
    --show-rc                       \
    --keep-hourly   2               \
    --keep-daily    7               \
    --keep-weekly   4               \
    --keep-monthly  6               \

prune_exit=$?

# use highest exit code as global exit code
global_exit=$(( backup_exit > prune_exit ? backup_exit : prune_exit ))

if [ ${global_exit} -eq 0 ]; then
    INTERPRETATION="success"
elif [ ${global_exit} -eq 1 ]; then
    INTERPRETATION="warning"
else
    INTERPRETATION="error"
fi

info "Backup and/or Prune finished with" $INTERPRETATION

# Add Logging Routine
LOG_FOLDER=/var/log/custom
LOG_FILE_PATH=$LOG_FOLDER/backup.log

if [ ! -f $LOG_FOLDER ]; then
    mkdir -p $LOG_FOLDER
    chown -R 1000:1000 $LOG_FOLDER
fi

if [ ! -f $LOG_FILE_PATH ]; then
    echo "date,exit_code,exit_code_message" > $LOG_FILE_PATH
    chown 1000:1000 $LOG_FILE_PATH
fi

echo $(date),${global_exit},${INTERPRETATION} >> $LOG_FILE_PATH 
chown -R 1000:1000 $BORG_REPO

# Exit Program
exit ${global_exit}

