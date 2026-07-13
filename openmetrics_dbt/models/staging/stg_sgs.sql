SELECT
    b.indicator,
    b.data AS date,
    b.valor AS value,
    i.display_name,
    i.source,
    i.frequency,
    i.unit
FROM {{ source('bronze', 'bronze_sgs') }} AS b

LEFT JOIN {{ ref('indicators') }} AS i
    ON b.indicator = i.indicator