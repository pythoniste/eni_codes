import asyncio
from subprocess import CalledProcessError


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


async def getstatutoutput(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if not stdout:
        result = stderr.strip()
    elif not stderr:
        result = stdout.strip()
    else:
        result = stdout + b"\n" + stderr

    return proc.returncode, result.decode()


async def getoutput(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if not stdout:
        result = stderr.strip()
    elif not stderr:
        result = stdout.strip()
    else:
        result = stdout + b"\n" + stderr

    return result.decode()


async def check_output(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise CalledProcessError(proc.returncode, cmd)

    if not stdout:
        result = stderr.strip()
    elif not stderr:
        result = stdout.strip()
    else:
        result = stdout + b"\n" + stderr

    return result.decode()

from time import time
async def main():
    starting_time = time()
    await asyncio.gather(
        run('ls'),
        run('ls existe pas'),
        getstatutoutput('ls'),
        getstatutoutput('ls existepas'),
        getoutput('ls'),
        getoutput('ls existepas'),
        check_output('ls'),
    )
    print(f"Time spent: {time() - starting_time}") 


if __name__ == "__main__":
    asyncio.run(run('ls'))
    asyncio.run(run('ls existepas'))
    asyncio.run(getstatutoutput('ls'))
    asyncio.run(getstatutoutput('ls existepas'))
    asyncio.run(getoutput('ls'))
    asyncio.run(getoutput('ls existepas'))
    asyncio.run(check_output('ls'))
    asyncio.run(check_output('ls existepas'))

    asyncio.run(main())



starting_time = time()
subprocess.run('ls', shell=True),
subprocess.run('ls existepas', shell=True),
subprocess.getstatusoutput('ls'),
subprocess.getstatusoutput('ls existepas'),
subprocess.getoutput('ls'),
subprocess.getoutput('ls existepas'),
subprocess.check_output('ls', shell=True),
print(f"Time spent: {time() - starting_time}") 

