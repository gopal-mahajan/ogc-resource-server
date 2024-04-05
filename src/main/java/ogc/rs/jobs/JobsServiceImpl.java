package ogc.rs.jobs;

import io.vertx.core.Future;
import io.vertx.core.Promise;
import io.vertx.core.json.JsonArray;
import io.vertx.core.json.JsonObject;
import io.vertx.pgclient.PgPool;
import io.vertx.sqlclient.Row;
import io.vertx.sqlclient.Tuple;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;
import ogc.rs.common.Constants;
import ogc.rs.metering.MeteringServiceImpl;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class JobsServiceImpl implements JobsService {
  private static final Logger LOGGER = LogManager.getLogger(JobsServiceImpl.class);
  private final PgPool pgPool;
  private final JsonObject config;

  public JobsServiceImpl(PgPool pgPool, JsonObject config) {
    this.pgPool = pgPool;
    this.config = config;
  }

  @Override
  public Future<JsonObject> getStatus(JsonObject requestBody) {
    LOGGER.info("Trying to get status");

    Promise<JsonObject> promise = Promise.promise();
    String jobId = requestBody.getString("jobId");
    String userId = requestBody.getString("userId");
    pgPool.withConnection(
      sqlClient -> sqlClient.preparedQuery("Select * from jobs_table where id=$1")
        .execute(Tuple.of(jobId)).map(s -> s.iterator().next()).onSuccess(row -> {
          if (row.getValue("user_id").toString().equals(userId)) {
            JsonObject result = row.toJson();
            result.remove("output");
            JsonObject links = new JsonObject();
            links.put("href", config.getString("hostName").concat("/jobs/").concat(jobId));
            links.put("rel", "self");
            links.put("title", row.getJsonObject("input").getString("title"));
            result.remove("input");
            result.put("links", links);
            promise.complete(result);
          } else {
            LOGGER.error("Job does not belong to the specified user");
            promise.fail(Constants.processException404);
          }
        }).onFailure(failureHandler -> {
          LOGGER.error(failureHandler.toString());
          promise.fail(Constants.processException404);
        }));

    return promise.future();
  }

}



