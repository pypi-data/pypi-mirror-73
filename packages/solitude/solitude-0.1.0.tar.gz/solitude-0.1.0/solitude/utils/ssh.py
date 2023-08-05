import subprocess as sp
import paramiko
import time


def command_remote(server, username, password, cmd_to_execute):
    """
    Executes a command over ssh

    Implementation relies on paramiko
    """
    print(cmd_to_execute)
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    return "".join(ssh_stdout.readlines()), "".join(ssh_stderr.readlines())


def start_worker(server, username, password, gpus, user="sil", ticket="", version="latest"):
    if isinstance(gpus, list):
        gpus = " ".join(gpus)
    cmd = "~/start-docker.py --user {} --ticket {} --run oni:11500/sil/sil_worker_node:{} --ports --gpus {}".format(user, ticket, version, gpus)
    return command_remote(server, username, password, cmd)


def kill_worker(server, username, password, gpu):
    a = command_remote(server, username, password, "~/list-dockers.py")[0].split("\n")
    for e in a:
        if " using GPUs: " in e:
            if str(gpu) in e.split(" using GPUs: ")[1].strip():
                key = str(e.split(" by ")[0]).strip()
                return command_remote(server, username, password, "docker kill {}".format(key))
    return None


def list_dockers(server, username, password):
    for e in command_remote(server, username, password, "~/list-dockers.py")[0].split("\n"):
        if "Stopped containers:" in e:
            break
        print(e)


def start_worker_and_tag(server, username, password, gpu, client, user, ticket, version="latest"):
    result = start_worker(server, username, password, gpu, user=user, ticket=ticket, version=version)
    print(result)
    if "Started container" in result[0]:
        mid = result[0].split("Started container: ")[1][:12] + "_1"
        tag = "{}_{}".format(server, gpu)
        time.sleep(3)
        print(client.tag_worker(mid, tag), mid, tag)


def schedule_job(server, username, password, job, user="sil", ticket="5429", time="160", container="oni:11500/sil/sil_job_worker:latest",
                 req_gpu_mem='11g', req_mem='32g', gpu_count=1, req_cpus=4, req_gpu=None, high_priority=False, interactive=False, reservation=None, node=None):
    command = '~/c-submit'
    if req_gpu_mem is not None:
        command += ' --require-gpu-mem={}'.format(req_gpu_mem)
    if req_mem is not None:
        command += ' --require-mem={}'.format(req_mem)
    if gpu_count is not None:
        command += ' --gpu-count={}'.format(gpu_count)
    if req_cpus is not None:
        command += ' --require-cpus={}'.format(req_cpus)
    if req_gpu is not None:
        command += ' --require-gpu={}'.format(req_gpu)
    if reservation is not None:
        command += ' --reservation={}'.format(reservation)
    if node is not None:
        command += ' --node={}'.format(node)
    command += ' --priority=' + ('high' if high_priority else 'low')
    if interactive:
        command += ' --interactive'
    command += ' {} {} {} {} {}'.format(user, ticket, time, container, job)
    return command_remote(server, username, password, command)[0]


def get_job_list(server, username, password):
    return command_remote(server, username, password, "~/c-list")[0]


def get_job_log(server, username, password, job_id):
    lines = get_job_list(server, username, password).split("\n")
    midx, jobx = lines[0].find("Machine"), lines[0].find("Job ID")
    lookup = {}
    for l in lines[1:]:
        if len(l.strip()) > 0:
            lookup[int(l[jobx:].split(" ")[0])] = l[midx:].split(" ")[0]
    return command_remote(lookup[job_id], username, password, "cat ~/slurm-{}.out".format(job_id))[0]


def stop_job(server, username, password, job_id):
    return command_remote(server, username, password, "~/c-stop {}".format(job_id))[0]


def get_job_task_info(server, username, password, user="sil"):
    l = get_job_list(server, username, password)
    l = l.split("\n")
    idx = l[0].find("Runtime")
    job_idx = l[0].find("Job ID")

    userrows = [e for e in l[1:] if user in e]
    logids = [int(e[job_idx:job_idx + 6]) for e in userrows]
    running = ["RUNNING" in e for e in userrows]
    runtime = [e[idx:idx + 10] for e in userrows]
    results = []
    for j, i in enumerate(logids):
        if "None assigned" not in userrows[j]:
            lg = get_job_log(server, username, password, i)
            idx = lg.find("Extra arguments: ")
            idxe = lg.find("\n", idx)
            cmd = lg[idx + 17:idxe].strip()
            results.append((i, running[j], runtime[j], cmd))
