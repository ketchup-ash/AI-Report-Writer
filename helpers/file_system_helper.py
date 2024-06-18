import os

def get_required_env(
        env_name: str
) -> str:
    env_value = os.environ.get(env_name)
    if env_value is None:
        raise Exception(f'Missing environment variable: {env_name}')
    return env_value