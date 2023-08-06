import os
import platform

import time

from .installer import PostgresInstaller, Shell
from remo_app.remo.stores.version_store import Version
from .log import Log


class WindowsPostgresInstaller(PostgresInstaller):
    def _stop(self) -> bool:
        return Shell.ok("pg_ctl stop", show_command=False, show_output=False)

    def restart(self) -> bool:
        self._set_env_vars()
        if not Shell.ok("pg_ctl --version", show_command=False, show_output=False):
            Log.exit('failed to restart postgres, pg_ctl was not found in the PATH')

        return Shell.ok("pg_ctl restart")

    def is_running(self):
        return Shell.ok("psql -U postgres -l", show_command=False, show_output=False)

    def _launch(self):
        Log.msg("Launching postgres ... ", nl=False)

        for _ in range(3):
            if Shell.ok("pg_ctl start", show_command=False, show_output=False):
                break
            time.sleep(2)

        if not Shell.ok("pg_ctl status", show_command=False, show_output=False):
            Log.exit('failed to launch postgres')
        Log.msg("done")

    def _install(self):
        Shell.run("scoop install postgresql@12.2", show_output=False)
        self._set_env_vars()

    def _create_db_and_user(self, dbname, username, password):
        Shell.run(
            f"""psql -U postgres -c "create user {username} with encrypted password '{password}';" """,
            show_output=False,
        )
        Shell.run(f"""psql -U postgres -c "create database {dbname};" """, show_output=False)
        Shell.run(
            f"""psql -U postgres -c "grant all privileges on database {dbname} to {username};" """,
            show_output=False,
        )
        return self.db_params(database=dbname, user=username, password=password)

    def _drop_db(self, database: str):
        Shell.run(f"""psql -U postgres -c "drop database {database};" """, show_output=True)

    def _is_installed(self) -> bool:
        if self._is_psql_in_path():
            return True

        self._set_env_vars()
        return self._is_psql_in_path()

    def _is_psql_in_path(self) -> bool:
        return Shell.ok("psql --version", show_command=False, show_output=False)

    def _get_postgres_dir(self) -> str:
        for path in (
            '%PROGRAMFILES%\\PostgreSQL',
            '%PROGRAMFILES(x86)%\\PostgreSQL',
            '%USERPROFILE%\\scoop\\apps\\postgresql',
        ):
            full_path = os.path.expandvars(path)
            if os.path.exists(full_path):
                return full_path

    def _get_postgres_version_dir(self, postgres_dir: str) -> str:
        current = os.path.join(postgres_dir, 'current')
        if os.path.exists(current):
            return current

        versions = os.listdir(postgres_dir)
        if len(versions) > 1:
            versions.sort(key=Version.to_num, reverse=True)
        return os.path.join(postgres_dir, versions[0])

    def _set_env_vars(self):
        path = self._get_postgres_dir()
        if not path:
            return

        postgres = self._get_postgres_version_dir(path)

        bin = os.path.join(postgres, 'bin')
        if os.path.exists(bin) and bin not in os.environ["PATH"]:
            os.environ["PATH"] = bin + os.pathsep + os.environ["PATH"]

        data = os.path.join(postgres, 'data')
        if os.getenv('PGDATA') and not os.path.exists(os.getenv('PGDATA')):
            os.environ.pop('PGDATA')
        if os.path.exists(data) and not os.getenv('PGDATA'):
            os.environ['PGDATA'] = data


class LinuxPostgresInstaller(PostgresInstaller):
    def _stop(self) -> bool:
        return Shell.ok('sudo systemctl stop postgresql', show_command=False, show_output=False)

    def restart(self) -> bool:
        return Shell.ok('sudo systemctl restart postgresql')

    def _is_installed(self):
        return Shell.ok("psql --version", show_command=False, show_output=False)

    def _install(self):
        Shell.run('sudo apt-get install -y -qq postgresql', show_output=False)

    def is_running(self):
        return Shell.ok("service postgresql status", show_command=False, show_output=False)

    def _launch(self):
        Log.msg("Launching postgres ... ", nl=False)
        Shell.run('sudo systemctl start postgresql', show_command=False, show_output=False)
        Log.msg("done")

    def _drop_db(self, database: str):
        Shell.run(f"""sudo -u postgres psql -c "drop database {database};" """, show_output=True)

    def _create_db_and_user(self, dbname, username, password):
        Shell.run(
            f"""sudo -u postgres psql -c "create user {username} with encrypted password '{password}';" """,
            show_output=False,
        )
        Shell.run(f"""sudo -u postgres psql -c "create database {dbname};" """, show_output=False)
        Shell.run(
            f"""sudo -u postgres psql -c "grant all privileges on database {dbname} to {username};" """,
            show_output=False,
        )
        return self.db_params(database=dbname, user=username, password=password)


class MacPostgresInstaller(PostgresInstaller):
    postgres_version = 'postgresql@10'

    def _get_postgres_homebrew_mxcl(self) -> str:
        postgres_exe_path = Shell.output('which', 'postgres', show_command=False)
        postgres_dir = os.path.dirname(os.path.dirname(postgres_exe_path))
        files = list(filter(lambda name: name.startswith('homebrew'), os.listdir(postgres_dir)))
        if files:
            return os.path.join(postgres_dir, files[0])

    def _stop(self) -> bool:
        return Shell.ok(f'brew services stop {self._get_postgres_version()}', show_command=False, show_output=False)

    def restart(self) -> bool:
        return Shell.ok(f'brew services restart {self._get_postgres_version()}')

    def _is_installed(self):
        if Shell.ok("postgres --version", show_command=False, show_output=False):
            return True
        self._add_postgres_to_path()
        return Shell.ok("postgres --version", show_command=False, show_output=False)

    def _get_postgres_version(self):
        files = list(filter(lambda name: name.startswith('postgresql'), os.listdir('/usr/local/Cellar/')))
        if files:
            return files[0]
        return self.postgres_version

    def _add_postgres_to_path(self):
        postgres_version = self._get_postgres_version()
        if os.path.exists(f'/usr/local/opt/{postgres_version}/bin'):
            os.environ['PATH'] = f"/usr/local/opt/{postgres_version}/bin:{os.getenv('PATH')}"

    def is_running(self):
        if Shell.ok("psql -l", show_command=False, show_output=False):
            return True
        self._add_postgres_to_path()
        return Shell.ok("psql -l", show_command=False, show_output=False)

    def _install(self):
        Shell.run(f'brew install {self._get_postgres_version()}', show_output=False)
        shell_exe_path = os.getenv('SHELL')
        shell_name = os.path.basename(shell_exe_path)
        shell_rc_path = os.path.expanduser(f'~/.{shell_name}rc')
        Shell.run(f"""echo 'export PATH="/usr/local/opt/{self._get_postgres_version()}/bin:$PATH"' >> {shell_rc_path}""")
        self._add_postgres_to_path()

    def _launch(self):
        homebrew_mxcl = self._get_postgres_homebrew_mxcl()
        if not homebrew_mxcl:
            Log.exit_msg("Failed to launch postgres server, please start it manually.")

        Log.msg("Launching postgres ... ", nl=False)
        Shell.run(f'launchctl load {homebrew_mxcl}', show_command=False, show_output=False)

        for _ in range(5):
            if self.is_running():
                break
            time.sleep(1)

        if not self.is_running():
            Shell.ok(f'brew services start {self._get_postgres_version()}', show_command=False, show_output=False)
            for _ in range(5):
                if self.is_running():
                    break
                time.sleep(1)

        if self.is_running():
            Log.msg("done")
        else:
            Log.exit("Failed to launch postgres")

    def _drop_db(self, database: str):
        Shell.run(f'dropdb {database}', show_output=True)

    def _create_db_and_user(self, dbname, username, password):
        Shell.run('createdb $USER', show_output=False)
        Shell.run(
            f"""psql -c "create user {username} with encrypted password '{password}';" """, show_output=False
        )
        Shell.run(f'createdb {dbname} -O {username}', show_output=False)
        return self.db_params(database=dbname, user=username, password=password)


def get_instance() -> PostgresInstaller:
    installer = installers.get(platform.system())
    if not installer:
        Log.exit_warn(f'current operation system - {platform.system()}, is not supported.')

    return installer


installers = {
    'Windows': WindowsPostgresInstaller(),
    'Linux': LinuxPostgresInstaller(),
    'Darwin': MacPostgresInstaller(),
}
