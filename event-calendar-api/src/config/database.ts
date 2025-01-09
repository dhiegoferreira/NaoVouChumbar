export const dbConfig = {
	url: process.env.DATABASE_URL,
	ssl: process.env.NODE_ENV === 'production'

}
