import { useEffect, useState } from "react";
import API from "../services/api";

function Dossiers() {
  const [dossiers, setDossiers] = useState([]);
  const [loading, setLoading] = useState(true);

  // 🔹 Charger les dossiers
  const fetchDossiers = async () => {
    try {
      const response = await API.get("/dossiers/");
      setDossiers(response.data);
    } catch (error) {
      console.error("Erreur récupération dossiers :", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDossiers();
  }, []);

  // 🔹 Upload document
  const handleUpload = async (id, file) => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      await API.post(`/dossiers/${id}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      alert("Document uploadé avec succès ✅");

      // 🔁 Refresh des dossiers
      fetchDossiers();

    } catch (error) {
      console.error("Erreur upload :", error);
      alert("Erreur lors de l'upload ❌");
    }
  };

  if (loading) {
    return <p className="text-center mt-5">Chargement des dossiers...</p>;
  }

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Mes Dossiers</h2>

      {dossiers.length === 0 ? (
        <div className="alert alert-info">
          Aucun dossier trouvé.
        </div>
      ) : (
        <div className="row">
          {dossiers.map((d) => (
            <div key={d.id} className="col-md-6 mb-4">
              <div className="card shadow-sm">
                <div className="card-body">

                  <h5 className="card-title">
                    Dossier #{d.id}
                  </h5>

                  <p><strong>Véhicule ID:</strong> {d.vehicule_id}</p>
                  <p><strong>Type:</strong> {d.type}</p>

                  <p>
                    <strong>Status:</strong>{" "}
                    <span className={
                      d.status === "VALIDE"
                        ? "badge bg-success"
                        : d.status === "REFUSE"
                        ? "badge bg-danger"
                        : "badge bg-warning text-dark"
                    }>
                      {d.status}
                    </span>
                  </p>

                  {/* Upload autorisé seulement si EN_ATTENTE */}
                  {d.status === "EN_ATTENTE" && (
                    <div className="mt-3">
                      <label className="form-label">
                        Ajouter un document :
                      </label>
                      <input
                        type="file"
                        className="form-control"
                        onChange={(e) =>
                          handleUpload(d.id, e.target.files[0])
                        }
                      />
                    </div>
                  )}

                  {/* Message si validé */}
                  {d.status === "VALIDE" && (
                    <div className="alert alert-success mt-3">
                       Dossier validé par l'administrateur
                    </div>
                  )}

                  {/* Message si refusé */}
                  {d.status === "REFUSE" && (
                    <div className="alert alert-danger mt-3">
                       Dossier refusé par l'administrateur
                    </div>
                  )}

                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Dossiers;