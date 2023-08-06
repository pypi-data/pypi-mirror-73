[](https://www.archlinux.org/)

  * [Home](https://www.archlinux.org/)
  * [Packages](https://www.archlinux.org/packages/)
  * [Forums](https://bbs.archlinux.org/)
  * [Wiki](https://wiki.archlinux.org/)
  * [Bugs](https://bugs.archlinux.org/)
  * [Security](https://security.archlinux.org/)
  * [AUR](https://aur.archlinux.org/)
  * [Download](https://www.archlinux.org/download/)

# PostgreSQL

From ArchWiki

(Redirected from [Postgres](/index.php?title=Postgres&redirect=no "Postgres"))

Jump to navigation Jump to search

Related articles

  * [PhpPgAdmin](/index.php/PhpPgAdmin "PhpPgAdmin")

[PostgreSQL](https://www.postgresql.org/) is an open source, community driven,
standard compliant object-relational database system.

## Contents

  * 1 Installation
  * 2 Initial configuration
  * 3 Create your first database/user
  * 4 Familiarize with PostgreSQL
    * 4.1 Access the database shell
  * 5 Optional configuration
    * 5.1 Restricts access rights to the database superuser by default
    * 5.2 Configure PostgreSQL to be accessible exclusively through UNIX Sockets
    * 5.3 Configure PostgreSQL to be accessible from remote hosts
    * 5.4 Configure PostgreSQL authenticate against PAM
    * 5.5 Change default data directory
    * 5.6 Change default encoding of new databases to UTF-8
  * 6 Graphical tools
  * 7 Upgrading PostgreSQL
    * 7.1 pg_upgrade
    * 7.2 Manual dump and reload
  * 8 Troubleshooting
    * 8.1 Improve performance of small transactions
    * 8.2 Prevent disk writes when idle
    * 8.3 pgAdmin 4 issues after upgrade to PostgreSQL 12

## Installation

[![Tango-edit-clear.png](/images/8/87/Tango-edit-
clear.png)](/index.php/File:Tango-edit-clear.png)**This article or section
needs language, wiki syntax or style improvements.
See[Help:Style](/index.php/Help:Style "Help:Style") for reference.**[![Tango-
edit-clear.png](/images/8/87/Tango-edit-clear.png)](/index.php/File:Tango-
edit-clear.png)

**Reason:** Don't duplicate [sudo](/index.php/Sudo "Sudo") and
[su](/index.php/Su "Su"). (Discuss in
[Talk:PostgreSQL#](https://wiki.archlinux.org/index.php/Talk:PostgreSQL))

[Install](/index.php/Install "Install") the
[postgresql](https://www.archlinux.org/packages/?name=postgresql) package. It
will also create a system user called _postgres_.

**Warning:** See #Upgrading PostgreSQL for necessary steps before installing
new versions of the PostgreSQL packages.

**Note:** Commands that should be run as the _postgres_ user are prefixed by
`[postgres]$` in this article.

You can switch to the PostgreSQL user by executing the following command:

  * If you have [sudo](/index.php/Sudo "Sudo") and are in [sudoers](/index.php/Sudoers "Sudoers"):

    
    
    
    $ sudo -iu postgres

  * Otherwise using [su](/index.php/Su "Su"):

    
    
    
    $ su
    # su -l postgres
    

See [sudo(8)](https://jlk.fjfi.cvut.cz/arch/manpages/man/sudo.8) or
[su(1)](https://jlk.fjfi.cvut.cz/arch/manpages/man/su.1) for their usage.

## Initial configuration

Before PostgreSQL can function correctly, the database cluster must be
initialized:

    
    
    [postgres]$ initdb -D /var/lib/postgres/data
    

Where `-D` is the default location where the database cluster must be stored
(see #Change default data directory if you want to use a different one).

Note that by default, the locale and the encoding for the database cluster are
derived from your current environment (using
[$LANG](/index.php/Locale#LANG:_default_locale "Locale") value).
[[1]](https://www.postgresql.org/docs/current/static/locale.html) However,
depending on your settings and use cases this might not be what you want, and
you can override the defaults using:

  * `--locale= _locale_`, where _locale_ is to be chosen amongst the system's [available locales](/index.php/Locale#Generating_locales "Locale");
  * `-E _encoding_` for the encoding (which must match the chosen locale);

Example:

    
    
    [postgres]$ initdb --locale=en_US.UTF-8 -E UTF8 -D /var/lib/postgres/data
    

Many lines should now appear on the screen with several ending by `... ok`:

    
    
    The files belonging to this database system will be owned by user "postgres".
    This user must also own the server process.
    
    The database cluster will be initialized with locale "en_US.UTF-8".
    The default database encoding has accordingly been set to "UTF8".
    The default text search configuration will be set to "english".
    
    Data page checksums are disabled.
    
    fixing permissions on existing directory /var/lib/postgres/data ... ok
    creating subdirectories ... ok
    selecting default max_connections ... 100
    selecting default shared_buffers ... 128MB
    selecting dynamic shared memory implementation ... posix
    creating configuration files ... ok
    running bootstrap script ... ok
    performing post-bootstrap initialization ... ok
    syncing data to disk ... ok
    
    WARNING: enabling "trust" authentication for local connections
    You can change this by editing pg_hba.conf or using the option -A, or
    --auth-local and --auth-host, the next time you run initdb.
    
    Success. You can now start the database server using:
    
        pg_ctl -D /var/lib/postgres/ -l logfile start
    

If these are the kind of lines you see, then the process succeeded. Return to
the regular user using `exit`.

**Note:** To read more about this `WARNING`, see #Restricts access rights to
the database superuser by default.

**Tip:** If you change the root to something other than `/var/lib/postgres`,
you will have to [edit](/index.php/Edit "Edit") the service file. If the root
is under `home`, make sure to set `ProtectHome` to false.

**Warning:**

  * If the database resides on a [Btrfs](/index.php/Btrfs "Btrfs") file system, you should consider disabling [Copy-on-Write](/index.php/Btrfs#Copy-on-Write_\(CoW\) "Btrfs") for the directory before creating any database.
  * If the database resides on a [ZFS](/index.php/ZFS "ZFS") file system, you should consult [ZFS#Databases](/index.php/ZFS#Databases "ZFS") before creating any database.

Finally, [start](/index.php/Start "Start") and [enable](/index.php/Enable
"Enable") the `postgresql.service`.

## Create your first database/user

**Tip:** If you create a PostgreSQL user with the same name as your Linux
username, it allows you to access the PostgreSQL database shell without having
to specify a user to login (which makes it quite convenient).

Become the postgres user. Add a new database user using the
[createuser](https://www.postgresql.org/docs/current/static/app-
createuser.html) command:

    
    
    [postgres]$ createuser --interactive
    

Create a new database over which the above user has read/write privileges
using the [createdb](https://www.postgresql.org/docs/current/static/app-
createdb.html) command (execute this command from your login shell if the
database user has the same name as your Linux user, otherwise add `-O
_database-username_` to the following command):

    
    
    $ createdb myDatabaseName
    

**Tip:** If you did not grant your new user database creation privileges, add
`-U postgres` to the previous command.

## Familiarize with PostgreSQL

### Access the database shell

Become the postgres user. Start the primary database shell,
[psql](https://www.postgresql.org/docs/current/static/app-psql.html), where
you can do all your creation of databases/tables, deletion, set permissions,
and run raw SQL commands. Use the `-d` option to connect to the database you
created (without specifying a database, `psql` will try to access a database
that matches your username).

    
    
    [postgres]$ psql -d myDatabaseName
    

Some helpful commands:

Get help:

    
    
    => \help
    

Connect to a particular database:

    
    
    => \c <database>
    

List all users and their permission levels:

    
    
    => \du
    

Show summary information about all tables in the current database:

    
    
    => \dt
    

Exit/quit the `psql` shell:

    
    
    => \q or CTRL+d
    

There are of course many more meta-commands, but these should help you get
started. To see all meta-commands run:

    
    
    => \?
    

## Optional configuration

The PostgreSQL database server configuration file is `postgresql.conf`. This
file is located in the data directory of the server, typically
`/var/lib/postgres/data`. This folder also houses the other main configuration
files, including the `pg_hba.conf` which defines authentication settings, for
both local users and other hosts ones.

**Note:** By default, this folder will not be browsable or searchable by a
regular user. This is why `find` and `locate` are not finding the
configuration files.

### Restricts access rights to the database superuser by default

The defaults `pg_hba.conf` **allow any local user to connect as any database
user** , including the database superuser. This is likely not what you want,
so in order to restrict global access to the _postgres_ user, change the
following line:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    
    # "local" is for Unix domain socket connections only
    local   all             all                                     trust

To:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    
    # "local" is for Unix domain socket connections only
    local   all             postgres                                peer

You might later add additional lines depending on your needs or software ones.

### Configure PostgreSQL to be accessible exclusively through UNIX Sockets

In the connections and authentications section of your configuration, set:

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    listen_addresses = ''

This will disable network listening completely. After this you should
[restart](/index.php/Restart "Restart") `postgresql.service` for the changes
to take effect.

### Configure PostgreSQL to be accessible from remote hosts

In the connections and authentications section, set the `listen_addresses`
line to your needs:

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    listen_addresses = 'localhost, _my_local_ip_address'_

You can use `'*'` to listen on all available addresses.

**Note:** PostgreSQL uses TCP port `5432` by default for remote connections.
Make sure this port is open in your [firewall](/index.php/Firewall "Firewall")
and able to receive incoming connections. You can also change it in the
configuration file, right below `listen_addresses`

Then add a line like the following to the authentication config:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    # IPv4 local connections:
    host    all             all             _ip_address_ /32   md5

where `_ip_address_` is the IP address of the remote client.

See the documentation for
[pg_hba.conf](https://www.postgresql.org/docs/current/static/auth-pg-hba-
conf.html).

**Note:** Neither sending your plain password nor the md5 hash (used in the
example above) over the Internet is secure if it is not done over an SSL-
secured connection. See [Secure TCP/IP Connections with
SSL](https://www.postgresql.org/docs/current/static/ssl-tcp.html) for how to
configure PostgreSQL with SSL.

After this you should [restart](/index.php/Restart "Restart")
`postgresql.service` for the changes to take effect.

For troubleshooting take a look in the server log file:

    
    
    $ journalctl -u postgresql.service
    

### Configure PostgreSQL authenticate against PAM

PostgreSQL offers a number of authentication methods. If you would like to
allow users to authenticate with their system password, additional steps are
necessary. First you need to enable [PAM](/index.php/PAM "PAM") for the
connection.

For example, the same configuration as above, but with PAM enabled:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # IPv4 local connections:
    host   all   all   _my_remote_client_ip_address_ /32   pam

The PostgreSQL server is however running without root privileges and will not
be able to access `/etc/shadow`. We can work around that by allowing the
postgres group to access this file:

    
    
    # setfacl -m g:postgres:r /etc/shadow
    

### Change default data directory

The default directory where all your newly created databases will be stored is
`/var/lib/postgres/data`. To change this, follow these steps:

Create the new directory and make the postgres user its owner:

    
    
    # mkdir -p /pathto/pgroot/data
    # chown -R postgres:postgres /pathto/pgroot
    

Become the postgres user, and initialize the new cluster:

    
    
    [postgres]$ initdb -D /pathto/pgroot/data
    

[Edit](/index.php/Edit "Edit") `postgresql.service` to create a drop-in file
and override the `Environment` and `PIDFile` settings. For example:

    
    
    [Service]
    Environment=PGROOT= _/pathto/pgroot_
    PIDFile= _/pathto/pgroot/_ data/postmaster.pid
    

If you want to use `/home` directory for default directory or for tablespaces,
add one more line in this file:

    
    
    ProtectHome=false
    

### Change default encoding of new databases to UTF-8

**Note:** If you ran `initdb` with `-E UTF8` or while using an UTF-8 locale,
these steps are not required.

When creating a new database (e.g. with `createdb blog`) PostgreSQL actually
copies a template database. There are two predefined templates: `template0` is
vanilla, while `template1` is meant as an on-site template changeable by the
administrator and is used by default. In order to change the encoding of a new
database, one of the options is to change on-site `template1`. To do this, log
into PostgreSQL shell (`psql`) and execute the following:

First, we need to drop `template1`. Templates cannot be dropped, so we first
modify it so it is an ordinary database:

    
    
    UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';
    

Now we can drop it:

    
    
    DROP DATABASE template1;
    

The next step is to create a new database from `template0`, with a new default
encoding:

    
    
    CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UNICODE';
    

Now modify `template1` so it is actually a template:

    
    
    UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';
    

Optionally, if you do not want anyone connecting to this template, set
`datallowconn` to `FALSE`:

    
    
    UPDATE pg_database SET datallowconn = FALSE WHERE datname = 'template1';
    

**Note:** This last step can create problems when upgrading via `pg_upgrade`.

Now you can create a new database:

    
    
    [postgres]$ createdb blog
    

If you log back in to `psql` and check the databases, you should see the
proper encoding of your new database:

    
    
    \l
    
    
                                  List of databases
      Name    |  Owner   | Encoding  | Collation | Ctype |   Access privileges
    -----------+----------+-----------+-----------+-------+----------------------
    blog      | postgres | UTF8      | C         | C     |
    postgres  | postgres | SQL_ASCII | C         | C     |
    template0 | postgres | SQL_ASCII | C         | C     | =c/postgres
                                                         : postgres=CTc/postgres
    template1 | postgres | UTF8      | C         | C     |
    

## Graphical tools

  * **[phpPgAdmin](/index.php/PhpPgAdmin "PhpPgAdmin")** -- Web-based administration tool for PostgreSQL.

    <http://phppgadmin.sourceforge.net> || [phppgadmin](https://www.archlinux.org/packages/?name=phppgadmin)

  * **pgAdmin** -- Comprehensive design and management GUI for PostgreSQL.

    <https://www.pgadmin.org/> || [pgadmin3](https://aur.archlinux.org/packages/pgadmin3/)AUR or [pgadmin4](https://www.archlinux.org/packages/?name=pgadmin4)

  * **pgModeler** -- Graphical schema designer for PostgreSQL.

    <https://pgmodeler.io/> || [pgmodeler](https://aur.archlinux.org/packages/pgmodeler/)AUR

For tools supporting multiple DBMSs, see [List of
applications/Documents#Database
tools](/index.php/List_of_applications/Documents#Database_tools "List of
applications/Documents").

## Upgrading PostgreSQL

[![Tango-edit-clear.png](/images/8/87/Tango-edit-
clear.png)](/index.php/File:Tango-edit-clear.png)**This article or section
needs language, wiki syntax or style improvements.
See[Help:Style](/index.php/Help:Style "Help:Style") for reference.**[![Tango-
edit-clear.png](/images/8/87/Tango-edit-clear.png)](/index.php/File:Tango-
edit-clear.png)

**Reason:** Don't show basic systemctl commands, etc. (Discuss in
[Talk:PostgreSQL#](https://wiki.archlinux.org/index.php/Talk:PostgreSQL))

[![Tango-view-fullscreen.png](/images/3/38/Tango-view-
fullscreen.png)](/index.php/File:Tango-view-fullscreen.png)**This article or
section needs expansion.**[![Tango-view-fullscreen.png](/images/3/38/Tango-
view-fullscreen.png)](/index.php/File:Tango-view-fullscreen.png)

**Reason:** How to upgrade when using third party extensions? (Discuss in
[Talk:PostgreSQL#pg_upgrade problem if extensions (like postgis) are
used](https://wiki.archlinux.org/index.php/Talk:PostgreSQL#pg_upgrade_problem_if_extensions_\(like_postgis\)_are_used))

Upgrading major PostgreSQL versions requires some extra maintenance.

**Note:**

  * Official PostgreSQL [upgrade documentation](https://www.postgresql.org/docs/current/static/upgrading.html) should be followed.
  * From version `10.0` onwards PostgreSQL [changed its versioning scheme](https://www.postgresql.org/about/news/1786/). Earlier upgrade from version `9. _x_` to `9. _y_` was considered as major upgrade. Now upgrade from version `10. _x_` to `10. _y_` is considered as minor upgrade and upgrade from version `10. _x_` to `11. _y_` is considered as major upgrade.

**Warning:** The following instructions could cause data loss. Do not run the
commands below blindly, without understanding what they do. [Backup
database](https://www.postgresql.org/docs/current/static/backup.html) first.

Get the currently used database version via

    
    
    # cat /var/lib/postgres/data/PG_VERSION
    

To ensure you do not accidentally upgrade the database to an incompatible
version, it is recommended to [skip
updates](/index.php/Pacman#Skip_package_from_being_upgraded "Pacman") to the
PostgreSQL packages:

    
    
    /etc/pacman.conf
    
    
    ...
    IgnorePkg = postgresql postgresql-libs
    ...

Minor version upgrades are safe to perform. However, if you do an accidental
upgrade to a different major version, you might not be able to access any of
your data. Always check the [PostgreSQL home
page](https://www.postgresql.org/) to be sure of what steps are required for
each upgrade. For a bit about why this is the case, see the [versioning
policy](https://www.postgresql.org/support/versioning).

There are two main ways to upgrade your PostgreSQL database. Read the official
documentation for details.

### pg_upgrade

For those wishing to use `pg_upgrade`, a [postgresql-old-
upgrade](https://www.archlinux.org/packages/?name=postgresql-old-upgrade)
package is available that will always run one major version behind the real
PostgreSQL package. This can be installed side-by-side with the new version of
PostgreSQL. To upgrade from older versions of PostgreSQL there are AUR
packages available:
[postgresql-96-upgrade](https://aur.archlinux.org/packages/postgresql-96-upgrade/)AUR,
[postgresql-95-upgrade](https://aur.archlinux.org/packages/postgresql-95-upgrade/)AUR,
[postgresql-94-upgrade](https://aur.archlinux.org/packages/postgresql-94-upgrade/)AUR,
[postgresql-93-upgrade](https://aur.archlinux.org/packages/postgresql-93-upgrade/)AUR,
[postgresql-92-upgrade](https://aur.archlinux.org/packages/postgresql-92-upgrade/)AUR.
Read the
[pg_upgrade(1)](https://jlk.fjfi.cvut.cz/arch/manpages/man/pg_upgrade.1) man
page to understand what actions it performs.

Note that the databases cluster directory does not change from version to
version, so before running `pg_upgrade`, it is necessary to rename your
existing data directory and migrate into a new directory. The new databases
cluster must be initialized, as described in the #Installation section.

When you are ready, stop the postgresql service, upgrade the following
packages: [postgresql](https://www.archlinux.org/packages/?name=postgresql),
[postgresql-libs](https://www.archlinux.org/packages/?name=postgresql-libs),
and [postgresql-old-
upgrade](https://www.archlinux.org/packages/?name=postgresql-old-upgrade).
Finally upgrade the databases cluster.

Stop and make sure PostgreSQL is stopped:

    
    
    # systemctl stop postgresql.service
    # systemctl status postgresql.service
    

Make sure that PostgresSQL was stopped correctly. If it failed, `pg_upgrade`
will fail too.

Upgrade the packages:

    
    
    # pacman -S postgresql postgresql-libs postgresql-old-upgrade
    

Rename the databases cluster directory, and create an empty one:

    
    
    # mv /var/lib/postgres/data /var/lib/postgres/olddata
    # mkdir /var/lib/postgres/data /var/lib/postgres/tmp
    # chown postgres:postgres /var/lib/postgres/data /var/lib/postgres/tmp
    [postgres]$ cd /var/lib/postgres/tmp
    [postgres]$ initdb -D /var/lib/postgres/data
    

Upgrade the cluster, replacing `_PG_VERSION_` below, with the old PostgreSQL
version number (e.g. `11`):

    
    
    [postgres]$ pg_upgrade -b /opt/pgsql- _PG_VERSION_ /bin -B /usr/bin -d /var/lib/postgres/olddata -D /var/lib/postgres/data
    

`pg_upgrade` will perform the upgrade and create some scripts in
`/var/lib/postgres/tmp/`. Follow the instructions given on screen and act
accordingly. You may delete the `/var/lib/postgres/tmp` directory once the
upgrade is completely over.

If necessary, adjust the configuration files of new cluster (e.g.
`pg_hba.conf` and `postgresql.conf`) to match the old cluster.

Start the cluster:

    
    
    # systemctl start postgresql.service
    

### Manual dump and reload

You could also do something like this (after the upgrade and install of
[postgresql-old-upgrade](https://www.archlinux.org/packages/?name=postgresql-
old-upgrade)).

**Note:**

  * Below are the commands for upgrading from PostgreSQL 11. You can find similar commands in `/opt/` for your version of PostgreSQL cluster, provided you have matching version of [postgresql-old-upgrade](https://www.archlinux.org/packages/?name=postgresql-old-upgrade) package installed.
  * If you had customized your `pg_hba.conf` file, you may have to temporarily modify it to allow full access to old database cluster from local system. After upgrade is complete set your customization to new database cluster as well and [restart](/index.php/Restart "Restart") `postgresql.service`.

    
    
    # systemctl stop postgresql.service
    # mv /var/lib/postgres/data /var/lib/postgres/olddata
    # mkdir /var/lib/postgres/data
    # chown postgres:postgres /var/lib/postgres/data
    [postgres]$ initdb -D /var/lib/postgres/data
    [postgres]$ /opt/pgsql-11/bin/pg_ctl -D /var/lib/postgres/olddata/ start
    [postgres]$ pg_dumpall -h /tmp -f /tmp/old_backup.sql
    [postgres]$ /opt/pgsql-11/bin/pg_ctl -D /var/lib/postgres/olddata/ stop
    # systemctl start postgresql.service
    [postgres]$ psql -f /tmp/old_backup.sql postgres
    

## Troubleshooting

### Improve performance of small transactions

If you are using PostgresSQL on a local machine for development and it seems
slow, you could try turning [synchronous_commit
off](https://www.postgresql.org/docs/current/static/runtime-config-
wal.html#GUC-SYNCHRONOUS-COMMIT) in the configuration. Beware of the
[caveats](https://www.postgresql.org/docs/current/static/runtime-config-
wal.html#GUC-SYNCHRONOUS-COMMIT), however.

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    synchronous_commit = off

### Prevent disk writes when idle

PostgreSQL periodically updates its internal "statistics" file. By default,
this file is stored on disk, which prevents disks from spinning down on
laptops and causes hard drive seek noise. It is simple and safe to relocate
this file to a memory-only file system with the following configuration
option:

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    stats_temp_directory = '/run/postgresql'

### pgAdmin 4 issues after upgrade to PostgreSQL 12

If you see errors about `string indices must be integers` when navigating the
tree on the left, or about `column rel.relhasoids does not exist` when viewing
the data, remove the server from the connection list in pgAdmin and add a
fresh server instance. pgAdmin will otherwise continue to treat the server as
a PostgreSQL 11 server resulting in these issues.

Retrieved from
"[https://wiki.archlinux.org/index.php?title=PostgreSQL&oldid=614721](https://wiki.archlinux.org/index.php?title=PostgreSQL&oldid=614721)"

[Category](/index.php/Special:Categories "Special:Categories"):

  * [Relational DBMSs](/index.php/Category:Relational_DBMSs "Category:Relational DBMSs")

Hidden categories:

  * [Pages or sections flagged with Template:Style](/index.php/Category:Pages_or_sections_flagged_with_Template:Style "Category:Pages or sections flagged with Template:Style")
  * [Pages or sections flagged with Template:Expansion](/index.php/Category:Pages_or_sections_flagged_with_Template:Expansion "Category:Pages or sections flagged with Template:Expansion")

## Navigation menu

### Personal tools

  * [Create account](/index.php?title=Special:CreateAccount&returnto=PostgreSQL "You are encouraged to create an account and log in; however, it is not mandatory")
  * [Log in](/index.php?title=Special:UserLogin&returnto=PostgreSQL "You are encouraged to log in; however, it is not mandatory \[o\]")

### Namespaces

  * [Page](/index.php/PostgreSQL "View the content page \[c\]")
  * [Discussion](/index.php/Talk:PostgreSQL "Discussion about the content page \[t\]")

###  Variants

### Views

  * [Read](/index.php/PostgreSQL)
  * [View source](/index.php?title=PostgreSQL&action=edit "This page is protected.
You can view its source \[e\]")

  * [View history](/index.php?title=PostgreSQL&action=history "Past revisions of this page \[h\]")

### More

###  Search

[](/index.php/Main_page "Visit the main page")

### Navigation

  * [Main page](/index.php/Main_page "Visit the main page \[z\]")
  * [Table of contents](/index.php/Table_of_contents)
  * [Getting involved](/index.php/Getting_involved "Various ways Archers can contribute to the community")
  * [Wiki news](/index.php/ArchWiki:News "The latest lowdown on the wiki")
  * [Random page](/index.php/Special:Random "Load a random page \[x\]")

### Interaction

  * [Help](/index.php/Category:Help "Wiki navigation, reading, and editing help")
  * [Contributing](/index.php/ArchWiki:Contributing)
  * [Recent changes](/index.php/Special:RecentChanges "A list of recent changes in the wiki \[r\]")
  * [Recent talks](https://wiki.archlinux.org/index.php/Special:RecentChanges?namespace=all-discussions)
  * [New pages](/index.php/Special:NewPages)
  * [Statistics](/index.php/ArchWiki:Statistics)
  * [Requests](/index.php/ArchWiki:Requests)

### Tools

  * [What links here](/index.php/Special:WhatLinksHere/PostgreSQL "A list of all wiki pages that link here \[j\]")
  * [Related changes](/index.php/Special:RecentChangesLinked/PostgreSQL "Recent changes in pages linked from this page \[k\]")
  * [Special pages](/index.php/Special:SpecialPages "A list of all special pages \[q\]")
  * [Printable version](/index.php?title=PostgreSQL&printable=yes "Printable version of this page \[p\]")
  * [Permanent link](/index.php?title=PostgreSQL&oldid=614721 "Permanent link to this revision of the page")
  * [Page information](/index.php?title=PostgreSQL&action=info "More information about this page")

### In other languages

  * [Italiano](https://wiki.archlinux.org/index.php/PostgreSQL_\(Italiano\) "PostgreSQL – italiano")
  * [日本語](https://wiki.archlinux.jp/index.php/PostgreSQL "PostgreSQL – 日本語")
  * [Русский](https://wiki.archlinux.org/index.php/PostgreSQL_\(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9\) "PostgreSQL – русский")
  * [Türkçe](https://wiki.archlinux.org/index.php/PostgreSQL_\(T%C3%BCrk%C3%A7e\) "PostgreSQL – Türkçe")
  * [中文（简体）‎](https://wiki.archlinux.org/index.php/PostgreSQL_\(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87\) "PostgreSQL – 中文（简体）‎")

  * This page was last edited on 21 May 2020, at 16:08.
  * Content is available under [GNU Free Documentation License 1.3 or later](http://www.gnu.org/copyleft/fdl.html) unless otherwise noted.

  * [Privacy policy](/index.php/ArchWiki:Privacy_policy "ArchWiki:Privacy policy")
  * [About ArchWiki](/index.php/ArchWiki:About "ArchWiki:About")
  * [Disclaimers](/index.php/ArchWiki:General_disclaimer "ArchWiki:General disclaimer")

  * 

[](https://www.archlinux.org/)

  * [Home](https://www.archlinux.org/)
  * [Packages](https://www.archlinux.org/packages/)
  * [Forums](https://bbs.archlinux.org/)
  * [Wiki](https://wiki.archlinux.org/)
  * [Bugs](https://bugs.archlinux.org/)
  * [Security](https://security.archlinux.org/)
  * [AUR](https://aur.archlinux.org/)
  * [Download](https://www.archlinux.org/download/)

# PostgreSQL

From ArchWiki

(Redirected from [Postgres](/index.php?title=Postgres&redirect=no "Postgres"))

Jump to navigation Jump to search

Related articles

  * [PhpPgAdmin](/index.php/PhpPgAdmin "PhpPgAdmin")

[PostgreSQL](https://www.postgresql.org/) is an open source, community driven,
standard compliant object-relational database system.

## Contents

  * 1 Installation
  * 2 Initial configuration
  * 3 Create your first database/user
  * 4 Familiarize with PostgreSQL
    * 4.1 Access the database shell
  * 5 Optional configuration
    * 5.1 Restricts access rights to the database superuser by default
    * 5.2 Configure PostgreSQL to be accessible exclusively through UNIX Sockets
    * 5.3 Configure PostgreSQL to be accessible from remote hosts
    * 5.4 Configure PostgreSQL authenticate against PAM
    * 5.5 Change default data directory
    * 5.6 Change default encoding of new databases to UTF-8
  * 6 Graphical tools
  * 7 Upgrading PostgreSQL
    * 7.1 pg_upgrade
    * 7.2 Manual dump and reload
  * 8 Troubleshooting
    * 8.1 Improve performance of small transactions
    * 8.2 Prevent disk writes when idle
    * 8.3 pgAdmin 4 issues after upgrade to PostgreSQL 12

## Installation

[![Tango-edit-clear.png](/images/8/87/Tango-edit-
clear.png)](/index.php/File:Tango-edit-clear.png)**This article or section
needs language, wiki syntax or style improvements.
See[Help:Style](/index.php/Help:Style "Help:Style") for reference.**[![Tango-
edit-clear.png](/images/8/87/Tango-edit-clear.png)](/index.php/File:Tango-
edit-clear.png)

**Reason:** Don't duplicate [sudo](/index.php/Sudo "Sudo") and
[su](/index.php/Su "Su"). (Discuss in
[Talk:PostgreSQL#](https://wiki.archlinux.org/index.php/Talk:PostgreSQL))

[Install](/index.php/Install "Install") the
[postgresql](https://www.archlinux.org/packages/?name=postgresql) package. It
will also create a system user called _postgres_.

**Warning:** See #Upgrading PostgreSQL for necessary steps before installing
new versions of the PostgreSQL packages.

**Note:** Commands that should be run as the _postgres_ user are prefixed by
`[postgres]$` in this article.

You can switch to the PostgreSQL user by executing the following command:

  * If you have [sudo](/index.php/Sudo "Sudo") and are in [sudoers](/index.php/Sudoers "Sudoers"):

    
    
    
    $ sudo -iu postgres

  * Otherwise using [su](/index.php/Su "Su"):

    
    
    
    $ su
    # su -l postgres
    

See [sudo(8)](https://jlk.fjfi.cvut.cz/arch/manpages/man/sudo.8) or
[su(1)](https://jlk.fjfi.cvut.cz/arch/manpages/man/su.1) for their usage.

## Initial configuration

Before PostgreSQL can function correctly, the database cluster must be
initialized:

    
    
    [postgres]$ initdb -D /var/lib/postgres/data
    

Where `-D` is the default location where the database cluster must be stored
(see #Change default data directory if you want to use a different one).

Note that by default, the locale and the encoding for the database cluster are
derived from your current environment (using
[$LANG](/index.php/Locale#LANG:_default_locale "Locale") value).
[[1]](https://www.postgresql.org/docs/current/static/locale.html) However,
depending on your settings and use cases this might not be what you want, and
you can override the defaults using:

  * `--locale= _locale_`, where _locale_ is to be chosen amongst the system's [available locales](/index.php/Locale#Generating_locales "Locale");
  * `-E _encoding_` for the encoding (which must match the chosen locale);

Example:

    
    
    [postgres]$ initdb --locale=en_US.UTF-8 -E UTF8 -D /var/lib/postgres/data
    

Many lines should now appear on the screen with several ending by `... ok`:

    
    
    The files belonging to this database system will be owned by user "postgres".
    This user must also own the server process.
    
    The database cluster will be initialized with locale "en_US.UTF-8".
    The default database encoding has accordingly been set to "UTF8".
    The default text search configuration will be set to "english".
    
    Data page checksums are disabled.
    
    fixing permissions on existing directory /var/lib/postgres/data ... ok
    creating subdirectories ... ok
    selecting default max_connections ... 100
    selecting default shared_buffers ... 128MB
    selecting dynamic shared memory implementation ... posix
    creating configuration files ... ok
    running bootstrap script ... ok
    performing post-bootstrap initialization ... ok
    syncing data to disk ... ok
    
    WARNING: enabling "trust" authentication for local connections
    You can change this by editing pg_hba.conf or using the option -A, or
    --auth-local and --auth-host, the next time you run initdb.
    
    Success. You can now start the database server using:
    
        pg_ctl -D /var/lib/postgres/ -l logfile start
    

If these are the kind of lines you see, then the process succeeded. Return to
the regular user using `exit`.

**Note:** To read more about this `WARNING`, see #Restricts access rights to
the database superuser by default.

**Tip:** If you change the root to something other than `/var/lib/postgres`,
you will have to [edit](/index.php/Edit "Edit") the service file. If the root
is under `home`, make sure to set `ProtectHome` to false.

**Warning:**

  * If the database resides on a [Btrfs](/index.php/Btrfs "Btrfs") file system, you should consider disabling [Copy-on-Write](/index.php/Btrfs#Copy-on-Write_\(CoW\) "Btrfs") for the directory before creating any database.
  * If the database resides on a [ZFS](/index.php/ZFS "ZFS") file system, you should consult [ZFS#Databases](/index.php/ZFS#Databases "ZFS") before creating any database.

Finally, [start](/index.php/Start "Start") and [enable](/index.php/Enable
"Enable") the `postgresql.service`.

## Create your first database/user

**Tip:** If you create a PostgreSQL user with the same name as your Linux
username, it allows you to access the PostgreSQL database shell without having
to specify a user to login (which makes it quite convenient).

Become the postgres user. Add a new database user using the
[createuser](https://www.postgresql.org/docs/current/static/app-
createuser.html) command:

    
    
    [postgres]$ createuser --interactive
    

Create a new database over which the above user has read/write privileges
using the [createdb](https://www.postgresql.org/docs/current/static/app-
createdb.html) command (execute this command from your login shell if the
database user has the same name as your Linux user, otherwise add `-O
_database-username_` to the following command):

    
    
    $ createdb myDatabaseName
    

**Tip:** If you did not grant your new user database creation privileges, add
`-U postgres` to the previous command.

## Familiarize with PostgreSQL

### Access the database shell

Become the postgres user. Start the primary database shell,
[psql](https://www.postgresql.org/docs/current/static/app-psql.html), where
you can do all your creation of databases/tables, deletion, set permissions,
and run raw SQL commands. Use the `-d` option to connect to the database you
created (without specifying a database, `psql` will try to access a database
that matches your username).

    
    
    [postgres]$ psql -d myDatabaseName
    

Some helpful commands:

Get help:

    
    
    => \help
    

Connect to a particular database:

    
    
    => \c <database>
    

List all users and their permission levels:

    
    
    => \du
    

Show summary information about all tables in the current database:

    
    
    => \dt
    

Exit/quit the `psql` shell:

    
    
    => \q or CTRL+d
    

There are of course many more meta-commands, but these should help you get
started. To see all meta-commands run:

    
    
    => \?
    

## Optional configuration

The PostgreSQL database server configuration file is `postgresql.conf`. This
file is located in the data directory of the server, typically
`/var/lib/postgres/data`. This folder also houses the other main configuration
files, including the `pg_hba.conf` which defines authentication settings, for
both local users and other hosts ones.

**Note:** By default, this folder will not be browsable or searchable by a
regular user. This is why `find` and `locate` are not finding the
configuration files.

### Restricts access rights to the database superuser by default

The defaults `pg_hba.conf` **allow any local user to connect as any database
user** , including the database superuser. This is likely not what you want,
so in order to restrict global access to the _postgres_ user, change the
following line:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    
    # "local" is for Unix domain socket connections only
    local   all             all                                     trust

To:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    
    # "local" is for Unix domain socket connections only
    local   all             postgres                                peer

You might later add additional lines depending on your needs or software ones.

### Configure PostgreSQL to be accessible exclusively through UNIX Sockets

In the connections and authentications section of your configuration, set:

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    listen_addresses = ''

This will disable network listening completely. After this you should
[restart](/index.php/Restart "Restart") `postgresql.service` for the changes
to take effect.

### Configure PostgreSQL to be accessible from remote hosts

In the connections and authentications section, set the `listen_addresses`
line to your needs:

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    listen_addresses = 'localhost, _my_local_ip_address'_

You can use `'*'` to listen on all available addresses.

**Note:** PostgreSQL uses TCP port `5432` by default for remote connections.
Make sure this port is open in your [firewall](/index.php/Firewall "Firewall")
and able to receive incoming connections. You can also change it in the
configuration file, right below `listen_addresses`

Then add a line like the following to the authentication config:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    # IPv4 local connections:
    host    all             all             _ip_address_ /32   md5

where `_ip_address_` is the IP address of the remote client.

See the documentation for
[pg_hba.conf](https://www.postgresql.org/docs/current/static/auth-pg-hba-
conf.html).

**Note:** Neither sending your plain password nor the md5 hash (used in the
example above) over the Internet is secure if it is not done over an SSL-
secured connection. See [Secure TCP/IP Connections with
SSL](https://www.postgresql.org/docs/current/static/ssl-tcp.html) for how to
configure PostgreSQL with SSL.

After this you should [restart](/index.php/Restart "Restart")
`postgresql.service` for the changes to take effect.

For troubleshooting take a look in the server log file:

    
    
    $ journalctl -u postgresql.service
    

### Configure PostgreSQL authenticate against PAM

PostgreSQL offers a number of authentication methods. If you would like to
allow users to authenticate with their system password, additional steps are
necessary. First you need to enable [PAM](/index.php/PAM "PAM") for the
connection.

For example, the same configuration as above, but with PAM enabled:

    
    
    /var/lib/postgres/data/pg_hba.conf
    
    
    # IPv4 local connections:
    host   all   all   _my_remote_client_ip_address_ /32   pam

The PostgreSQL server is however running without root privileges and will not
be able to access `/etc/shadow`. We can work around that by allowing the
postgres group to access this file:

    
    
    # setfacl -m g:postgres:r /etc/shadow
    

### Change default data directory

The default directory where all your newly created databases will be stored is
`/var/lib/postgres/data`. To change this, follow these steps:

Create the new directory and make the postgres user its owner:

    
    
    # mkdir -p /pathto/pgroot/data
    # chown -R postgres:postgres /pathto/pgroot
    

Become the postgres user, and initialize the new cluster:

    
    
    [postgres]$ initdb -D /pathto/pgroot/data
    

[Edit](/index.php/Edit "Edit") `postgresql.service` to create a drop-in file
and override the `Environment` and `PIDFile` settings. For example:

    
    
    [Service]
    Environment=PGROOT= _/pathto/pgroot_
    PIDFile= _/pathto/pgroot/_ data/postmaster.pid
    

If you want to use `/home` directory for default directory or for tablespaces,
add one more line in this file:

    
    
    ProtectHome=false
    

### Change default encoding of new databases to UTF-8

**Note:** If you ran `initdb` with `-E UTF8` or while using an UTF-8 locale,
these steps are not required.

When creating a new database (e.g. with `createdb blog`) PostgreSQL actually
copies a template database. There are two predefined templates: `template0` is
vanilla, while `template1` is meant as an on-site template changeable by the
administrator and is used by default. In order to change the encoding of a new
database, one of the options is to change on-site `template1`. To do this, log
into PostgreSQL shell (`psql`) and execute the following:

First, we need to drop `template1`. Templates cannot be dropped, so we first
modify it so it is an ordinary database:

    
    
    UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';
    

Now we can drop it:

    
    
    DROP DATABASE template1;
    

The next step is to create a new database from `template0`, with a new default
encoding:

    
    
    CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UNICODE';
    

Now modify `template1` so it is actually a template:

    
    
    UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';
    

Optionally, if you do not want anyone connecting to this template, set
`datallowconn` to `FALSE`:

    
    
    UPDATE pg_database SET datallowconn = FALSE WHERE datname = 'template1';
    

**Note:** This last step can create problems when upgrading via `pg_upgrade`.

Now you can create a new database:

    
    
    [postgres]$ createdb blog
    

If you log back in to `psql` and check the databases, you should see the
proper encoding of your new database:

    
    
    \l
    
    
                                  List of databases
      Name    |  Owner   | Encoding  | Collation | Ctype |   Access privileges
    -----------+----------+-----------+-----------+-------+----------------------
    blog      | postgres | UTF8      | C         | C     |
    postgres  | postgres | SQL_ASCII | C         | C     |
    template0 | postgres | SQL_ASCII | C         | C     | =c/postgres
                                                         : postgres=CTc/postgres
    template1 | postgres | UTF8      | C         | C     |
    

## Graphical tools

  * **[phpPgAdmin](/index.php/PhpPgAdmin "PhpPgAdmin")** -- Web-based administration tool for PostgreSQL.

    <http://phppgadmin.sourceforge.net> || [phppgadmin](https://www.archlinux.org/packages/?name=phppgadmin)

  * **pgAdmin** -- Comprehensive design and management GUI for PostgreSQL.

    <https://www.pgadmin.org/> || [pgadmin3](https://aur.archlinux.org/packages/pgadmin3/)AUR or [pgadmin4](https://www.archlinux.org/packages/?name=pgadmin4)

  * **pgModeler** -- Graphical schema designer for PostgreSQL.

    <https://pgmodeler.io/> || [pgmodeler](https://aur.archlinux.org/packages/pgmodeler/)AUR

For tools supporting multiple DBMSs, see [List of
applications/Documents#Database
tools](/index.php/List_of_applications/Documents#Database_tools "List of
applications/Documents").

## Upgrading PostgreSQL

[![Tango-edit-clear.png](/images/8/87/Tango-edit-
clear.png)](/index.php/File:Tango-edit-clear.png)**This article or section
needs language, wiki syntax or style improvements.
See[Help:Style](/index.php/Help:Style "Help:Style") for reference.**[![Tango-
edit-clear.png](/images/8/87/Tango-edit-clear.png)](/index.php/File:Tango-
edit-clear.png)

**Reason:** Don't show basic systemctl commands, etc. (Discuss in
[Talk:PostgreSQL#](https://wiki.archlinux.org/index.php/Talk:PostgreSQL))

[![Tango-view-fullscreen.png](/images/3/38/Tango-view-
fullscreen.png)](/index.php/File:Tango-view-fullscreen.png)**This article or
section needs expansion.**[![Tango-view-fullscreen.png](/images/3/38/Tango-
view-fullscreen.png)](/index.php/File:Tango-view-fullscreen.png)

**Reason:** How to upgrade when using third party extensions? (Discuss in
[Talk:PostgreSQL#pg_upgrade problem if extensions (like postgis) are
used](https://wiki.archlinux.org/index.php/Talk:PostgreSQL#pg_upgrade_problem_if_extensions_\(like_postgis\)_are_used))

Upgrading major PostgreSQL versions requires some extra maintenance.

**Note:**

  * Official PostgreSQL [upgrade documentation](https://www.postgresql.org/docs/current/static/upgrading.html) should be followed.
  * From version `10.0` onwards PostgreSQL [changed its versioning scheme](https://www.postgresql.org/about/news/1786/). Earlier upgrade from version `9. _x_` to `9. _y_` was considered as major upgrade. Now upgrade from version `10. _x_` to `10. _y_` is considered as minor upgrade and upgrade from version `10. _x_` to `11. _y_` is considered as major upgrade.

**Warning:** The following instructions could cause data loss. Do not run the
commands below blindly, without understanding what they do. [Backup
database](https://www.postgresql.org/docs/current/static/backup.html) first.

Get the currently used database version via

    
    
    # cat /var/lib/postgres/data/PG_VERSION
    

To ensure you do not accidentally upgrade the database to an incompatible
version, it is recommended to [skip
updates](/index.php/Pacman#Skip_package_from_being_upgraded "Pacman") to the
PostgreSQL packages:

    
    
    /etc/pacman.conf
    
    
    ...
    IgnorePkg = postgresql postgresql-libs
    ...

Minor version upgrades are safe to perform. However, if you do an accidental
upgrade to a different major version, you might not be able to access any of
your data. Always check the [PostgreSQL home
page](https://www.postgresql.org/) to be sure of what steps are required for
each upgrade. For a bit about why this is the case, see the [versioning
policy](https://www.postgresql.org/support/versioning).

There are two main ways to upgrade your PostgreSQL database. Read the official
documentation for details.

### pg_upgrade

For those wishing to use `pg_upgrade`, a [postgresql-old-
upgrade](https://www.archlinux.org/packages/?name=postgresql-old-upgrade)
package is available that will always run one major version behind the real
PostgreSQL package. This can be installed side-by-side with the new version of
PostgreSQL. To upgrade from older versions of PostgreSQL there are AUR
packages available:
[postgresql-96-upgrade](https://aur.archlinux.org/packages/postgresql-96-upgrade/)AUR,
[postgresql-95-upgrade](https://aur.archlinux.org/packages/postgresql-95-upgrade/)AUR,
[postgresql-94-upgrade](https://aur.archlinux.org/packages/postgresql-94-upgrade/)AUR,
[postgresql-93-upgrade](https://aur.archlinux.org/packages/postgresql-93-upgrade/)AUR,
[postgresql-92-upgrade](https://aur.archlinux.org/packages/postgresql-92-upgrade/)AUR.
Read the
[pg_upgrade(1)](https://jlk.fjfi.cvut.cz/arch/manpages/man/pg_upgrade.1) man
page to understand what actions it performs.

Note that the databases cluster directory does not change from version to
version, so before running `pg_upgrade`, it is necessary to rename your
existing data directory and migrate into a new directory. The new databases
cluster must be initialized, as described in the #Installation section.

When you are ready, stop the postgresql service, upgrade the following
packages: [postgresql](https://www.archlinux.org/packages/?name=postgresql),
[postgresql-libs](https://www.archlinux.org/packages/?name=postgresql-libs),
and [postgresql-old-
upgrade](https://www.archlinux.org/packages/?name=postgresql-old-upgrade).
Finally upgrade the databases cluster.

Stop and make sure PostgreSQL is stopped:

    
    
    # systemctl stop postgresql.service
    # systemctl status postgresql.service
    

Make sure that PostgresSQL was stopped correctly. If it failed, `pg_upgrade`
will fail too.

Upgrade the packages:

    
    
    # pacman -S postgresql postgresql-libs postgresql-old-upgrade
    

Rename the databases cluster directory, and create an empty one:

    
    
    # mv /var/lib/postgres/data /var/lib/postgres/olddata
    # mkdir /var/lib/postgres/data /var/lib/postgres/tmp
    # chown postgres:postgres /var/lib/postgres/data /var/lib/postgres/tmp
    [postgres]$ cd /var/lib/postgres/tmp
    [postgres]$ initdb -D /var/lib/postgres/data
    

Upgrade the cluster, replacing `_PG_VERSION_` below, with the old PostgreSQL
version number (e.g. `11`):

    
    
    [postgres]$ pg_upgrade -b /opt/pgsql- _PG_VERSION_ /bin -B /usr/bin -d /var/lib/postgres/olddata -D /var/lib/postgres/data
    

`pg_upgrade` will perform the upgrade and create some scripts in
`/var/lib/postgres/tmp/`. Follow the instructions given on screen and act
accordingly. You may delete the `/var/lib/postgres/tmp` directory once the
upgrade is completely over.

If necessary, adjust the configuration files of new cluster (e.g.
`pg_hba.conf` and `postgresql.conf`) to match the old cluster.

Start the cluster:

    
    
    # systemctl start postgresql.service
    

### Manual dump and reload

You could also do something like this (after the upgrade and install of
[postgresql-old-upgrade](https://www.archlinux.org/packages/?name=postgresql-
old-upgrade)).

**Note:**

  * Below are the commands for upgrading from PostgreSQL 11. You can find similar commands in `/opt/` for your version of PostgreSQL cluster, provided you have matching version of [postgresql-old-upgrade](https://www.archlinux.org/packages/?name=postgresql-old-upgrade) package installed.
  * If you had customized your `pg_hba.conf` file, you may have to temporarily modify it to allow full access to old database cluster from local system. After upgrade is complete set your customization to new database cluster as well and [restart](/index.php/Restart "Restart") `postgresql.service`.

    
    
    # systemctl stop postgresql.service
    # mv /var/lib/postgres/data /var/lib/postgres/olddata
    # mkdir /var/lib/postgres/data
    # chown postgres:postgres /var/lib/postgres/data
    [postgres]$ initdb -D /var/lib/postgres/data
    [postgres]$ /opt/pgsql-11/bin/pg_ctl -D /var/lib/postgres/olddata/ start
    [postgres]$ pg_dumpall -h /tmp -f /tmp/old_backup.sql
    [postgres]$ /opt/pgsql-11/bin/pg_ctl -D /var/lib/postgres/olddata/ stop
    # systemctl start postgresql.service
    [postgres]$ psql -f /tmp/old_backup.sql postgres
    

## Troubleshooting

### Improve performance of small transactions

If you are using PostgresSQL on a local machine for development and it seems
slow, you could try turning [synchronous_commit
off](https://www.postgresql.org/docs/current/static/runtime-config-
wal.html#GUC-SYNCHRONOUS-COMMIT) in the configuration. Beware of the
[caveats](https://www.postgresql.org/docs/current/static/runtime-config-
wal.html#GUC-SYNCHRONOUS-COMMIT), however.

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    synchronous_commit = off

### Prevent disk writes when idle

PostgreSQL periodically updates its internal "statistics" file. By default,
this file is stored on disk, which prevents disks from spinning down on
laptops and causes hard drive seek noise. It is simple and safe to relocate
this file to a memory-only file system with the following configuration
option:

    
    
    /var/lib/postgres/data/postgresql.conf
    
    
    stats_temp_directory = '/run/postgresql'

### pgAdmin 4 issues after upgrade to PostgreSQL 12

If you see errors about `string indices must be integers` when navigating the
tree on the left, or about `column rel.relhasoids does not exist` when viewing
the data, remove the server from the connection list in pgAdmin and add a
fresh server instance. pgAdmin will otherwise continue to treat the server as
a PostgreSQL 11 server resulting in these issues.

Retrieved from
"[https://wiki.archlinux.org/index.php?title=PostgreSQL&oldid=614721](https://wiki.archlinux.org/index.php?title=PostgreSQL&oldid=614721)"

[Category](/index.php/Special:Categories "Special:Categories"):

  * [Relational DBMSs](/index.php/Category:Relational_DBMSs "Category:Relational DBMSs")

Hidden categories:

  * [Pages or sections flagged with Template:Style](/index.php/Category:Pages_or_sections_flagged_with_Template:Style "Category:Pages or sections flagged with Template:Style")
  * [Pages or sections flagged with Template:Expansion](/index.php/Category:Pages_or_sections_flagged_with_Template:Expansion "Category:Pages or sections flagged with Template:Expansion")

## Navigation menu

### Personal tools

  * [Create account](/index.php?title=Special:CreateAccount&returnto=PostgreSQL "You are encouraged to create an account and log in; however, it is not mandatory")
  * [Log in](/index.php?title=Special:UserLogin&returnto=PostgreSQL "You are encouraged to log in; however, it is not mandatory \[o\]")

### Namespaces

  * [Page](/index.php/PostgreSQL "View the content page \[c\]")
  * [Discussion](/index.php/Talk:PostgreSQL "Discussion about the content page \[t\]")

###  Variants

### Views

  * [Read](/index.php/PostgreSQL)
  * [View source](/index.php?title=PostgreSQL&action=edit "This page is protected.
You can view its source \[e\]")

  * [View history](/index.php?title=PostgreSQL&action=history "Past revisions of this page \[h\]")

### More

###  Search

[](/index.php/Main_page "Visit the main page")

### Navigation

  * [Main page](/index.php/Main_page "Visit the main page \[z\]")
  * [Table of contents](/index.php/Table_of_contents)
  * [Getting involved](/index.php/Getting_involved "Various ways Archers can contribute to the community")
  * [Wiki news](/index.php/ArchWiki:News "The latest lowdown on the wiki")
  * [Random page](/index.php/Special:Random "Load a random page \[x\]")

### Interaction

  * [Help](/index.php/Category:Help "Wiki navigation, reading, and editing help")
  * [Contributing](/index.php/ArchWiki:Contributing)
  * [Recent changes](/index.php/Special:RecentChanges "A list of recent changes in the wiki \[r\]")
  * [Recent talks](https://wiki.archlinux.org/index.php/Special:RecentChanges?namespace=all-discussions)
  * [New pages](/index.php/Special:NewPages)
  * [Statistics](/index.php/ArchWiki:Statistics)
  * [Requests](/index.php/ArchWiki:Requests)

### Tools

  * [What links here](/index.php/Special:WhatLinksHere/PostgreSQL "A list of all wiki pages that link here \[j\]")
  * [Related changes](/index.php/Special:RecentChangesLinked/PostgreSQL "Recent changes in pages linked from this page \[k\]")
  * [Special pages](/index.php/Special:SpecialPages "A list of all special pages \[q\]")
  * [Printable version](/index.php?title=PostgreSQL&printable=yes "Printable version of this page \[p\]")
  * [Permanent link](/index.php?title=PostgreSQL&oldid=614721 "Permanent link to this revision of the page")
  * [Page information](/index.php?title=PostgreSQL&action=info "More information about this page")

### In other languages

  * [Italiano](https://wiki.archlinux.org/index.php/PostgreSQL_\(Italiano\) "PostgreSQL – italiano")
  * [日本語](https://wiki.archlinux.jp/index.php/PostgreSQL "PostgreSQL – 日本語")
  * [Русский](https://wiki.archlinux.org/index.php/PostgreSQL_\(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9\) "PostgreSQL – русский")
  * [Türkçe](https://wiki.archlinux.org/index.php/PostgreSQL_\(T%C3%BCrk%C3%A7e\) "PostgreSQL – Türkçe")
  * [中文（简体）‎](https://wiki.archlinux.org/index.php/PostgreSQL_\(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87\) "PostgreSQL – 中文（简体）‎")

  * This page was last edited on 21 May 2020, at 16:08.
  * Content is available under [GNU Free Documentation License 1.3 or later](http://www.gnu.org/copyleft/fdl.html) unless otherwise noted.

  * [Privacy policy](/index.php/ArchWiki:Privacy_policy "ArchWiki:Privacy policy")
  * [About ArchWiki](/index.php/ArchWiki:About "ArchWiki:About")
  * [Disclaimers](/index.php/ArchWiki:General_disclaimer "ArchWiki:General disclaimer")

  * 

