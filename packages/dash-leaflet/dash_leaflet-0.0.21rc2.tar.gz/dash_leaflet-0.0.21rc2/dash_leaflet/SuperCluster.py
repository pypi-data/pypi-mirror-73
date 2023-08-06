# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SuperCluster(Component):
    """A SuperCluster component.
LayerGroup is a wrapper of LayerGroup in react-leaflet.
It takes similar properties to its react-leaflet counterpart.

Keyword arguments:
- data (dict; optional): Data (consider using url for better performance).
- url (string; optional): Url to data (use instead of data for better performance).
- format (a value equal to: "geojson", "geobuf"; default "geojson"): Data format.
- options (dict; optional): Options passed to SuperCluster, https://github.com/mapbox/supercluster.
- zoomToBoundsOnClick (boolean; default True): If true, zoom on cluster click.
- id (string; optional): The ID used to identify this component in Dash callbacks
- n_clicks (number; default 0): Dash callback property. Number of times the marker has been clicked
- marker_click (dict; optional): Last feature clicked."""
    @_explicitize_args
    def __init__(self, data=Component.UNDEFINED, url=Component.UNDEFINED, format=Component.UNDEFINED, options=Component.UNDEFINED, zoomToBoundsOnClick=Component.UNDEFINED, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, marker_click=Component.UNDEFINED, **kwargs):
        self._prop_names = ['data', 'url', 'format', 'options', 'zoomToBoundsOnClick', 'id', 'n_clicks', 'marker_click']
        self._type = 'SuperCluster'
        self._namespace = 'dash_leaflet'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['data', 'url', 'format', 'options', 'zoomToBoundsOnClick', 'id', 'n_clicks', 'marker_click']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SuperCluster, self).__init__(**args)
