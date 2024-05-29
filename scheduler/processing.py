import math
from time import time
from multiprocessing import Process


from client import ApiClient


def split_load(dn_list, thread_count):
    buckets = []
    current = []

    domain_name_per_bucket = math.ceil(len(dn_list) / thread_count)

    bucket_index = 0
    for i in range(len(dn_list)):
        current.append(dn_list[i])
        bucket_index += 1

        if bucket_index == domain_name_per_bucket:
            buckets.append(current)
            current = []
            bucket_index = 0

    if len(current) > 0:
        buckets.append(current)

    return buckets


def resolve_all(client: ApiClient, thread_count):
    t1 = time()

    client.login()
    print("logged in")

    dn_list = client.dn_list()
    print(f"retrieved {len(dn_list)} domain to resolve")

    repartition_buckets = split_load(dn_list, thread_count)
    response_list = []

    def resolve_domain_name(name, bucket):
        for domain_name in bucket:
            print(f"{name} - resolving {domain_name}")

            status_code = client.dn_update(domain_name)
            response_list.append(
                {"domain_name": domain_name, "response": status_code == 200}
            )

    thread_list = []
    for i in range(len(repartition_buckets)):
        thread_bucket = repartition_buckets[i]
        thread_name = f"thread_{i}"
        thread_list.append(
            Process(target=resolve_domain_name, args=(thread_name, thread_bucket))
        )

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    success_list = [x["response"] for x in response_list]
    print(f"success: {success_list.count(True)} / {len(success_list)}")

    t2 = time()
    delta = round(t1 - t2)
    print(f"took {delta}s")
