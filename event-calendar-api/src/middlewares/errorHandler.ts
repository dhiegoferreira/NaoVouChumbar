import { AppError } from "../utils/erros";
import { Request, Response, NextFunction } from "express";
import { logger } from "../utils/logger";

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: "error",
      message: err.message,
    });
  }

  logger.error(err.stack);

  return res.status(500).json({
    status: "error",
    message: "Internal server error",
  });
};
