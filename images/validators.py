LABEL_SHAPE_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'required': [
        'endX',
        'endY',
        'startY',
        'startX',
    ],
    'properties': {
        'endX': {'type': 'integer', 'exclusiveMinimum': 0},
        'endY': {'type': 'integer', 'exclusiveMinimum': 0},
        'startY': {'type': 'integer', 'minimum': 0},
        'startX': {'type': 'integer', 'minimum': 0},
    },
}

LABEL_META_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'required': [
        'confirmed',
        'confidence_percent',
    ],
    'properties': {
        'confirmed': {'type': 'boolean'},
        'confidence_percent': {
            'type': 'number',
            'minimum': 0,
            'maximum': 100,
        },
    },
}
