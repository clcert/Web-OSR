from operator import itemgetter

# from graphs.models import Http80, Http443, Http8000, Http8080

# port_dict = {
#     '80': Http80,
#     '443': Http443,
#     '8000': Http8000,
#     '8080': Http8080
# }
#
#
# def filter_by_name(data, names):
#     filtered_list = list()
#
#     for name in names:
#         total = 0
#         for elem in data:
#             if name == elem[0]:
#                 total = elem[1]
#                 break
#         filtered_list.append((name, total))
#     return filtered_list
#
#
# def complete_bars_chart(value_name, value_list):
#     """
#     :type value_list: list
#     :type value_name: set
#     """
#     new_set = value_name - set([i[0] for i in value_list])
#     for elem in new_set:
#         value_list.append((elem, 0))
#
#     return value_list
#
#
# def add_other(data):
#     sum = 0
#     for elem in data:
#         sum += elem[1]
#     data.append(('Other', 1 - sum))
#
#     return data
#
#
# def accumulate(mongo_collections, query, sum_value=1, reverse=True, with_none=True, percentage=False):
#     freqs = mongo_collections.aggregate({'$group': {'_id': '$' + query, 'total': {'$sum': sum_value}}})
#
#     freqs_dict = dict()
#     for freq in freqs:
#         if with_none or freq['_id'] is not None:
#             freqs_dict[freq['_id']] = freq['total']
#
#     if percentage:
#         sum = 0
#         for key, value in freqs_dict.iteritems():
#             sum += value
#
#         sum = float(sum)
#         for key, value in freqs_dict.iteritems():
#             freqs_dict[key] = value / sum
#     return sorted(freqs_dict.items(), key=itemgetter(1), reverse=reverse)
#
#
# def version_web_server(port, scan, version):
#     version_data = None
#     if version:
#         version_data = add_other(accumulate(port_dict[port].objects(date=scan, metadata__service__product=version),
#                                             'metadata.service.version', percentage=True)[:9])
#     return version_data


class CountSet:

    def __init__(self, name, total):
        self.name = name
        self.total = total

    def __str__(self):
        return 'name: ' + self.name + ' total: ' + self.total

    @staticmethod
    def getKey(count_set):
        return count_set.total


def count(queryset, by='name'):
    query_count = dict()
    query_list = list()

    for query in queryset:
        if query[by] not in query_count:
            query_count[query[by]] = 1
        else:
            query_count[query[by]] += 1

    for k, v in query_count.iteritems():
        query_list.append(CountSet(k, v))

    return sorted(query_list, key=CountSet.getKey, reverse=True)



def date_to_yyyy_mm_dd(date):
    return str(date.year) + '-' + str(date.month) + '-' + str(date.day)
