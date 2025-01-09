export const appConfig = {
	port: process.env.PORT || 3000,
	env: process.env.NODE_ENV || 'development',
	corsOrigins: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3000']

}
