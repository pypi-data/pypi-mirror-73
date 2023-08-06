"""Filterstest for Property Filtering."""


from django_filters import Filter, FilterSet
from django_property_filter.filters import EXPLICIST_ONLY_FILTERS


class PropertyFilterSet(FilterSet):
    """Generic Filterset for Property Filters."""

    def __init__(self, *args, **kwargs):
        """Construct a PropertyFilterSet."""
        super().__init__(*args, **kwargs)
        self._setup_property_filters()

    def _add_filter(self, filter_class, property_fld_name, lookup_expr):
        """Add a Filter."""
        filter_name = F'{property_fld_name}__{lookup_expr}'
        self.filters[filter_name] = filter_class(property_fld_name=property_fld_name, lookup_expr=lookup_expr)

        # propagate the model and filterset to the filters
        self.filters[filter_name].model = self.queryset.model
        self.filters[filter_name].parent = self

    def _setup_property_filters(self):
        """Set up implicit filters."""
        if 'property_fields' in self.__class__.Meta.__dict__:  # pylint: disable=no-member
            prop_fields = self.__class__.Meta.__dict__['property_fields']  # pylint: disable=no-member

            for field in prop_fields:
                prop_fld_name = field[0]
                prop_filter_class = field[1]
                lookup_xpr_list = field[2]

                # Validate the attributes
                if not issubclass(prop_filter_class, Filter):
                    raise ValueError(F'{prop_filter_class} is not a subclass of {Filter}')

                if prop_filter_class in EXPLICIST_ONLY_FILTERS:
                    raise ValueError(F'{prop_filter_class} can only be declared Explicitely')

                if not isinstance(prop_fld_name, str):
                    raise ValueError(F'Property field "{prop_fld_name}" is not a str')

                if not isinstance(lookup_xpr_list, list) or not lookup_xpr_list:
                    raise ValueError(F'Lookup list "{lookup_xpr_list}" is not a valid list of lookups')

                # Create all Filters
                for lookup in lookup_xpr_list:
                    self._add_filter(prop_filter_class, prop_fld_name, lookup)
