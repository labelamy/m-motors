import { Navigate } from "react-router-dom";

function AdminRoute({ children }) {
  const user = JSON.parse(localStorage.getItem("currentUser"));

  console.log("ADMIN USER:", user); // DEBUG

  if (!user || user.role !== "admin") {
    return <Navigate to="/login" />;
  }

  return children;
}

export default AdminRoute;