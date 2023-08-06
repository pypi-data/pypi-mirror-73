#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq

from justice.parser import Parser


class Justice:
    SEARCH_URL = 'https://or.justice.cz/ias/ui/rejstrik?p::submit=x&\
-1.IFormSubmitListener-htmlContainer-top-form=&search={}'
    DETAIL_URL = 'https://or.justice.cz/ias/ui/rejstrik-firma.vysledky?subjektId={}&typ={}'
    DETAIL_TYPE_MAPPING = {'FULL': 'UPLNY', 'VALID': 'PLATNY'}

    def __init__(self, *, search_url=SEARCH_URL, detail_url=DETAIL_URL):
        self.SEARCH_URL = search_url
        self.DETAIL_URL = detail_url

    def search(self, string: str):
        doc = pq(url=self.SEARCH_URL.format(string))
        return Parser.parse_list_result(doc)

    def get_detail(self, subject_id: str, typ: str = "FULL"):
        """
        :param subject_id: ID of subject
        :param typ: FULL/VALID
        :return:
        """
        assert typ in self.DETAIL_TYPE_MAPPING
        doc = pq(url=self.DETAIL_URL.format(subject_id, self.DETAIL_TYPE_MAPPING[typ]))
        return Parser.parse_detail_result(doc)


if __name__ == '__main__':
    justice = Justice()
    # print(justice.search('08431116'))
    # print(justice.search('Seznam'))

    print(justice.get_detail('1060090'))
    print(justice.get_detail('676708'))
