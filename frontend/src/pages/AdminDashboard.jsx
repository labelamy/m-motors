import { useEffect, useState } from "react";
import API from "../services/api";

function AdminDashboard() {
  const [dossiers, setDossiers] = useState([]);

  useEffect(() => {
    API.get("/dossiers/")
      .then(res => setDossiers(res.data))
      .catch(err => console.error(err));
  }, []);

  const validate = async (id) => {
    await API.put(`/dossiers/${id}/validate`);
    window.location.reload();
  };

  return (
    <div className="container mt-5">
      <h2>Dashboard Admin</h2>

      {dossiers.map(d => (
        <div key={d.id} className="card mb-3">
          <div className="card-body">
            <p>Status: {d.status}</p>

            {d.status === "EN_ATTENTE" && (
              <>
                <button className="btn btn-success me-2" onClick={() => validate(d.id)}>
                  Valider
                </button>
              </>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default AdminDashboard;