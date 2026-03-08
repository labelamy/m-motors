import { Navigate } from "react-router-dom";
import { getCurrentUser } from "../services/auth";

function AdminRoute({ children }) {
  const user = getCurrentUser();

  if (!user || user.role !== "admin") {
    // pas connecté ou pas admin → login
    return <Navigate to="/login" />;
  }

  return children;
}

export default AdminRoute;