package ogc.rs.apiserver.router.gisentities.ogcfeatures;

import static ogc.rs.common.Constants.DEFAULT_SERVER_CRS;
import static ogc.rs.common.Constants.OAS_TOKEN_SECURITY;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import io.vertx.core.json.JsonArray;
import io.vertx.core.json.JsonObject;

/**
 * Class used to hold metadata for OGC Feature collections. 
 * 
 */
public class OgcFeaturesMetadata {

  private static final int OGC_LIMIT_PARAM_MIN_DEFAULT = 1;
  public static final int OGC_LIMIT_PARAM_MAX_DEFAULT = 5;

  public static final String OGC_OP_ID_PREFIX_REGEX = "^ogcFeature-.*";
  public static final String STAC_OP_ID_PREFIX_REGEX = "^itemlessStacCollection-.*";

  public static final String OGC_GET_COLLECTION_ITEMS_OP_ID_REGEX = "^ogcFeature-.*-get-features$";
  public static final String OGC_GET_SPECIFIC_FEATURE_OP_ID_REGEX =
      "^ogcFeature-.*-get-specific-feature$";

  private UUID id;
  private String title;
  private String description;
  private String datetimeKey;
  private List<String> supportedCrs = new ArrayList<String>();

  private PostgisGeomTypes geomType;

  private Map<String, OasTypes> attributes = new HashMap<String, OasTypes>();

  private final Supplier<String> OGC_GET_COLLECTION_ITEMS_SUMMARY =
      () -> "Get features from " + description;
  private final Supplier<String> OGC_GET_COLLECTION_ITEMS_OPERATION_ID =
      () -> "ogcFeature-" + id.toString() + "-get-features";
  private final Supplier<String> OGC_GET_COLLECTION_ITEMS_ENDPOINT =
      () -> "/collections/" + id.toString() + "/items";

  private final Supplier<String> OGC_GET_SPECIFIC_FEATURE_SUMMARY =
      () -> "Get single feature from " + description;
  private final Supplier<String> OGC_GET_SPECIFIC_FEATURE_OPERATION_ID =
      () -> "ogcFeature-" + id.toString() + "-get-specific-feature";
  private final Supplier<String> OGC_GET_SPECIFIC_FEATURE_ENDPOINT =
      () -> "/collections/" + id.toString() + "/items/{featureId}";

  @SuppressWarnings("unchecked")
  public OgcFeaturesMetadata(JsonObject obj) {
    id = UUID.fromString(obj.getString("id"));
    title = obj.getString("title", "Undefined title");
    description = obj.getString("description", "Undefined description");

    datetimeKey = obj.getString("datetime_key", null);
    supportedCrs = obj.getJsonArray("supported_crs", new JsonArray()).getList();

    geomType = PostgisGeomTypes
        .valueOf(obj.getString("geometry_type", PostgisGeomTypes.GEOMETRY.toString()));

    JsonObject attributeJson = obj.getJsonObject("attributes", new JsonObject());
    attributes = attributeJson.stream().collect(Collectors.toMap(i -> i.getKey(),
        i -> OasTypes.getOasTypeFromPostgresType(i.getValue().toString())));
  }
  
  public UUID getId() {
    return id;
  }

  /**
   * Generate OpenAPI JSON block for all OGC routes that this collection can have.
   * 
   * @param geomMaxLimitConf map specifying the max values for the <code>limit</code> parameter for
   *        a given geometry.
   * @return JSON object containing OpenAPI paths for all OGC routes for this collection.
   */
  public JsonObject generateOgcOasBlock(Map<PostgisGeomTypes, Integer> geomMaxLimitConf) {
    JsonObject block = new JsonObject();

    JsonObject crsQueryParam = new JsonObject().put("in", "query").put("name", "crs")
        .put("required", false).put("style", "form").put("explode", false)
        .put("schema", new JsonObject().put("type", "string").put("format", "uri")
            .put("default", DEFAULT_SERVER_CRS).put("enum", new JsonArray(supportedCrs)));

    JsonObject bboxCrsQueryParam = new JsonObject().put("in", "query").put("name", "bbox-crs")
        .put("required", false).put("style", "form").put("explode", false)
        .put("schema", new JsonObject().put("type", "string").put("format", "uri")
            .put("default", DEFAULT_SERVER_CRS).put("enum", new JsonArray(supportedCrs)));
    
    /* GET /collections/<collection-ID>/items */
    JsonObject collectionItemsApi = new JsonObject();

    collectionItemsApi.put("tags", new JsonArray().add(title));
    collectionItemsApi.put("summary", OGC_GET_COLLECTION_ITEMS_SUMMARY.get());
    collectionItemsApi.put("operationId", OGC_GET_COLLECTION_ITEMS_OPERATION_ID.get());
    
    collectionItemsApi.mergeIn(OAS_TOKEN_SECURITY);

    JsonArray parameters = new JsonArray();

    parameters.add(bboxCrsQueryParam).add(crsQueryParam)
        .add(new JsonObject().put("$ref", "#/components/parameters/bbox"));

    parameters.add(new JsonObject().put("$ref", "#/components/parameters/datetime"));

    int limitParamMaxValue = geomMaxLimitConf.get(geomType);
    int limitParamDefaultValue = limitParamMaxValue;

    JsonObject limitParam = new JsonObject().put("in", "query").put("name", "limit")
        .put("required", false).put("style", "form").put("explode", false).put("schema",
            new JsonObject().put("type", "integer").put("minimum", OGC_LIMIT_PARAM_MIN_DEFAULT)
                .put("maximum", limitParamMaxValue).put("default", limitParamDefaultValue));

    parameters.add(limitParam);
    parameters.add(new JsonObject().put("$ref", "#/components/parameters/offset"));
    
    parameters.addAll(generateOasParamsFromAttributes(attributes));

    collectionItemsApi.put("parameters", parameters);

    collectionItemsApi.put("responses",
        new JsonObject().put("200", new JsonObject().put("$ref", "#/components/responses/Features"))
            .put("400", new JsonObject().put("$ref", "#/components/responses/InvalidParameter"))
            .put("500", new JsonObject().put("$ref", "#/components/responses/ServerError")));

    block.put(OGC_GET_COLLECTION_ITEMS_ENDPOINT.get(),
        new JsonObject().put("get", collectionItemsApi));

    /* GET /collections/<collection-ID>/items/<feature-ID> */
    JsonObject featureSpecificApi = new JsonObject();

    featureSpecificApi.put("tags", new JsonArray().add(title));
    featureSpecificApi.put("summary", OGC_GET_SPECIFIC_FEATURE_SUMMARY.get());
    featureSpecificApi.put("operationId", OGC_GET_SPECIFIC_FEATURE_OPERATION_ID.get());

    featureSpecificApi.mergeIn(OAS_TOKEN_SECURITY);

    JsonObject featureIdQueryParam =
        new JsonObject().put("in", "path").put("name", "featureId").put("required", true)
            .put("schema", new JsonObject().put("type", OasTypes.INTEGER.toString().toLowerCase()));

    featureSpecificApi.put("parameters",
        new JsonArray().add(featureIdQueryParam).add(crsQueryParam));

    featureSpecificApi.put("responses",
        new JsonObject().put("200", new JsonObject().put("$ref", "#/components/responses/Feature"))
            .put("404", new JsonObject().put("$ref", "#/components/responses/NotFound"))
            .put("500", new JsonObject().put("$ref", "#/components/responses/ServerError")));

    block.put(OGC_GET_SPECIFIC_FEATURE_ENDPOINT.get(),
        new JsonObject().put("get", featureSpecificApi));

    return block;
  }

  /**
   * Generate OpenAPI query param definitions for all the attributes of a collection based on the
   * type of the attribute reported by PostgreSQL.
   * 
   * @param attributes map of attributes.
   * @return JSON array containing OpenAPI query parameter definitions for each attribute
   */
  private JsonArray generateOasParamsFromAttributes(Map<String, OasTypes> attributes) {
    JsonArray obj = new JsonArray();

    attributes.forEach((name, attr) -> {
      JsonObject json = new JsonObject();
      json.put("in", "query").put("name", name).put("required", false).put("style", "form")
          .put("explode", false);

      JsonObject schema = new JsonObject();

      schema.put("type", attr.toString().toLowerCase());
      if (OasTypes.ARRAY.equals(attr)) {
        // 'any' array type
        // https://swagger.io/docs/specification/data-models/data-types/#any
        schema.put("items", "{}");
      }

      json.put("schema", schema);
      obj.add(json);
    });

    return obj;
  }
}
