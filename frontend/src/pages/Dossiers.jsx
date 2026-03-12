import { useEffect, useState } from "react";
import API from "../services/api";

function Dossiers() {
  const [dossiers, setDossiers] = useState([]);
  const [loading, setLoading] = useState(true);

  // 🔹 Charger les dossiers
  const fetchDossiers = async () => {
    try {
      const response = await API.get("/dossiers/mes-dossiers");
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
      fetchDossiers();

    } catch (error) {
      console.error("Erreur upload :", error);
      alert("Erreur lors de l'upload ❌");
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case "VALIDE":
        return "badge bg-success";
      case "REFUSE":
        return "badge bg-danger";
      default:
        return "badge bg-warning text-dark";
    }
  };

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary"></div>
        <p className="mt-3">Chargement des dossiers...</p>
      </div>
    );
  }

  return (
    <div className="container py-5">

      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap">
        <h2 className="fw-bold">📁 Mes Dossiers</h2>
        <span className="text-muted">
          {dossiers.length} dossier(s)
        </span>
      </div>

      {dossiers.length === 0 ? (
        <div className="alert alert-info text-center shadow-sm">
          Aucun dossier trouvé.
        </div>
      ) : (
        <div className="row g-4">
          {dossiers.map((d) => (
            <div
              key={d.id}
              className="col-12 col-md-6 col-lg-4"
            >
              <div className="card h-100 shadow-sm border-0 dossier-card">

                <div className="card-body d-flex flex-column">

                  <h5 className="card-title fw-bold mb-3">
                    📄 Dossier #{d.id}
                  </h5>

                  <p className="mb-1">
                    <strong>Véhicule :</strong> {d.vehicule_id}
                  </p>

                  <p className="mb-2">
                    <strong>Type :</strong> {d.type}
                  </p>

                  <p className="mb-3">
                    <strong>Status :</strong>{" "}
                    <span className={getStatusBadge(d.status)}>
                      {d.status}
                    </span>
                  </p>

                  {/* Upload autorisé seulement si EN_ATTENTE */}
                  {d.status === "EN_ATTENTE" && (
                    <div className="mt-auto">
                      <label className="form-label">
                        📎 Ajouter un document
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
                  
                  {/* Lien vers le document s'il existe */}
                    {d.document_path && (
                      <div className="mt-2">
                        <a
                          href={`http://localhost:8000${d.document_path}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn btn-outline-secondary btn-sm"
                        >
                          📄 Voir document
                        </a>
                      </div>
                    )}

                  {/* Message validé */}
                  {d.status === "VALIDE" && (
                    <div className="alert alert-success mt-auto">
                      ✅ Dossier validé par l'administrateur
                    </div>
                  )}

                  {/* Message refusé */}
                  {d.status === "REFUSE" && (
                    <div className="alert alert-danger mt-auto">
                      ❌ Dossier refusé par l'administrateur
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