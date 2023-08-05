# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields, tree
from trytond.pool import Pool, PoolMeta
from trytond import backend
from trytond.transaction import Transaction
import logging

logger = logging.getLogger(__name__)

__all__ = ['Category']
__metaclass__ = PoolMeta


class Category(tree(separator=' / '), ModelSQL, ModelView):
    "Memo Category"
    __name__ = "pim_memos.category"
    
    name = fields.Char('Name', required=True, translate=True)
    parent = fields.Many2One('pim_memos.category', 'Parent', select=True)
    childs = fields.One2Many('pim_memos.category', 'parent', string='Children')

    @classmethod
    def __register__(cls, module_name):
        super(Category, cls).__register__(module_name)
        TableHandler = backend.get('TableHandler')
        # create index for 'create_uid'
        try :
            table = TableHandler(cls, module_name)
            table.index_action('create_uid', action='add')
        except :
            logger.warning('Category.__register__: index not created!')

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()
        cls._order.insert(0, ('name', 'ASC'))
        cls._error_messages.update({
                'delete_category': (u"The category '%s' has subcategories and therefore can not be deleted."),
                })

    @classmethod
    def validate(cls, categories):
        super(Category, cls).validate(categories)
        cls.check_recursion(categories)

    def get_rec_name(self, name):
        if self.parent:
            return self.parent.get_rec_name(name) + ' / ' + self.name
        else:
            return self.name

    @classmethod
    def search_rec_name(cls, name, clause):
        if isinstance(clause[2], str):
            values = clause[2].split('/')
            values.reverse()
            domain = []
            field = 'name'
            for name in values:
                domain.append((field, clause[1], name.strip()))
                field = 'parent.' + field
        else:
            domain = [('name',) + tuple(clause[1:])]
        ids = [w.id for w in cls.search(domain, order=[])]
        return [('parent', 'child_of', ids)]

    @classmethod
    def delete(cls, categories):
        if not categories:
            return True
        for i in categories:
            if len(i.childs) > 0:
                cls.raise_user_error('delete_category', (i.name))
        return super(Category, cls).delete(categories)

# ende Category
