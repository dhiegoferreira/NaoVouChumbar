export interface User {
  id: string;
  name: string;
  email: string;
  selectedEvents: Event[];
  createdAt: Date;
  updatedAt: Date;
}
