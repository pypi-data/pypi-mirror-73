from typing import AnyStr, List


def split_into_buckets(phrase: AnyStr, bucket_size: int) -> List[AnyStr]:
    bucket = []
    buckets = []
    bucket_length = 0
    for word in phrase.split():
        if len(word) > bucket_size:
            return []

        if bucket_length + len(bucket) + len(word) > bucket_size:
            buckets.append(" ".join(bucket))
            bucket.clear()
            bucket_length = 0

        bucket.append(word)
        bucket_length += len(word)

    buckets.append(" ".join(bucket))
    return buckets


def split_into_buckets(phrase: str, max_length: int):
    split_phrase = phrase.split()
    offset, count = 0, 0
    buckets = []
    while offset < len(split_phrase) and count < len(split_phrase):
        slice_n = split_phrase[offset: (len(split_phrase) - count)]
        if sum(map(len, slice_n)) + (len(slice_n) - 1) <= max_length:
            buckets.append(' '.join(slice_n))
            offset += len(slice_n)
            count = 0
        else:
            count += 1
    return buckets


assert split_into_buckets("she sells sea shells by the sea", 2) == []
assert split_into_buckets("ab bc cd", 1) == []
assert split_into_buckets("she sells sea shells by the sea", 10) == ["she sells", "sea shells", "by the sea"]
assert split_into_buckets("the mouse jumped over the cheese", 7) == ["the", "mouse", "jumped", "over", "the", "cheese"]
assert split_into_buckets("fairy dust coated the air", 20) == ["fairy dust coated", "the air"]
assert split_into_buckets("do the hokey pokey", 6) == ["do the", "hokey", "pokey"]
assert split_into_buckets("do the hokey pokey", 12) == ["do the hokey", "pokey"]
assert split_into_buckets("rich magnificent trees dotted the landscape", 12) == ["rich", "magnificent", "trees dotted", "the", "landscape"]
assert split_into_buckets("rich magnificent trees dotted the landscape", 15) == ["rich", "magnificent", "trees dotted", "the landscape"]
assert split_into_buckets("rich magnificent trees dotted the landscape", 18) == ["rich magnificent", "trees dotted the", "landscape"]
assert split_into_buckets("rich magnificent trees dotted the landscape", 22) == ["rich magnificent trees", "dotted the landscape"]
assert split_into_buckets("rich magnificent trees dotted the landscape", 40) == ["rich magnificent trees dotted the", "landscape"]
assert split_into_buckets("rich magnificent trees dotted the landscape", 43) == ["rich magnificent trees dotted the landscape"]
assert split_into_buckets("beep bo bee bop bee bo bo bop", 6) == ["beep", "bo bee", "bop", "bee bo", "bo bop"]
assert split_into_buckets("beep bo bee bop bee bo bo bop", 10) == ["beep bo", "bee bop", "bee bo bo", "bop"]
assert split_into_buckets("a b c d e", 3) == ["a b", "c d", "e"]
assert split_into_buckets("a b c d e", 2) == ["a", "b", "c", "d", "e"]
assert split_into_buckets("a b c d e", 1) == ["a", "b", "c", "d", "e"]
print("Successfully Passed All Tests For Challenge #14 - Word Buckets")