// src/server.ts
import { app } from "./app";
import { appConfig } from "./config/app";
import { logger } from "./utils/logger";

app.listen(appConfig.port, () => {
  logger.info(`Server running on port ${appConfig.port}`);
});
