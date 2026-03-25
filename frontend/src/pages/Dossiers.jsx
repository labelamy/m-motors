import { useEffect, useState } from "react";
import API from "../services/api";

function Dossiers() {
  const [dossiers, setDossiers] = useState([]);
  const [loading, setLoading] = useState(true);

  const DEFAULT_IMAGE = "/seed_images/default_car.jpg";

  const fetchDossiers = async () => {
    try {
      const response = await API.get("/dossiers/mes-dossiers");
      setDossiers(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDossiers();
  }, []);

  const handleUpload = async (id, file) => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      await API.post(`/dossiers/${id}/upload`, formData);
      fetchDossiers();
    } catch (error) {
      console.error(error);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case "VALIDE":
        return "bg-success";
      case "REFUSE":
        return "bg-danger";
      default:
        return "bg-warning text-dark";
    }
  };

  if (loading) {
    return <div className="text-center mt-5">Chargement...</div>;
  }

  return (
    <div className="container py-5">
      <h2 className="fw-bold mb-4">📁 Mes Dossiers</h2>

      <div className="row g-4">
        {dossiers.map((d) => (
          <div key={d.id} className="col-md-6 col-lg-4">

            <div className="card dossier-card border-0 shadow-sm">

              {/* IMAGE + OVERLAY */}
              <div className="image-container">
                <img
                  src={d.vehicule?.image_url || DEFAULT_IMAGE}
                  alt={d.vehicule?.model}
                  className="card-img-top"
                  onError={(e) => (e.target.src = DEFAULT_IMAGE)}
                />

                <div className="overlay">
                  <span className={`badge ${getStatusBadge(d.status)}`}>
                    {d.status}
                  </span>
                </div>
              </div>

              {/* CONTENU */}
              <div className="card-body">

                <h5 className="fw-bold">
                  {d.vehicule
                    ? `${d.vehicule.brand} ${d.vehicule.model}`
                    : "Véhicule"}
                </h5>

                <p className="text-muted mb-2">
                  Type : {d.type}
                </p>

                {d.status === "EN_ATTENTE" && (
                  <input
                    type="file"
                    className="form-control mt-2"
                    onChange={(e) =>
                      handleUpload(d.id, e.target.files[0])
                    }
                  />
                )}

                {d.document_path && (
                  <a
                    href={`http://localhost:8000${d.document_path}`}
                    target="_blank"
                    rel="noreferrer"
                    className="btn btn-sm btn-outline-dark mt-2"
                  >
                    📄 Voir document
                  </a>
                )}

              </div>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}

export default Dossiers;