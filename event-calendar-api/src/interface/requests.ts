export interface CreateEventDTO {
  subject: string;
  studentYear: number;
  year: number;
  semester: number;
  description: string;
  date: Date;
}

export interface SelectEventDTO {
  eventId: string[];
}
