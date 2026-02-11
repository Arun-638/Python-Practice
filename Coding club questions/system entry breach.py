# The hacker is trapped behind the first digital firewall.
# The firewall allows access only if a hidden continuous sequence of signals satisfies a modular condition.

# You are given: - An integer array nums representing encrypted signal packets - An integer k representing the firewall key

# Determine if the system contains a continuous subarray of size at least 2 whose sum is a multiple of k.

# Return true if such a subarray exists, otherwise return false.
def check_subarray_sum(nums, k):
    mod_map = {0: -1} 
    current_sum = 0

    for i in range(len(nums)):
        current_sum += nums[i]
        mod = current_sum % k if k != 0 else current_sum

        if mod in mod_map:
            if i - mod_map[mod] > 1:  
                return True
        else:
            mod_map[mod] = i

    return False

n = int(input())
nums = list(map(int, input().split()))
k = int(input())
print(check_subarray_sum(nums, k)) 