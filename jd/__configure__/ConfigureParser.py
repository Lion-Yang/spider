from scrapy import Selector


class ConfigureParser:

    def __init__(self, file_path):
        f = open(file_path)
        content = f.read()
        f.close()
        self.sel = Selector(text=content)

    def get_configures_by_type(self, type_name):
        con_dict = {}
        type_sel = self.sel.xpath('//{}'.format(type_name))
        for each in type_sel.xpath('*'):
            con_dict[each.root.tag] = each.root.text
        return con_dict

    def get_configure_by_tag_name(self, tag_name):
        return self.sel.xpath('//{}/text()'.format(tag_name)).extract()[0]

