import { useEffect, useState } from "react";
import API from "../services/api";

function Vehicules() {
  const [vehicules, setVehicules] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchVehicules = async () => {
    try {
      const res = await API.get("/vehicules/");
      setVehicules(res.data);
    } catch (error) {
      console.error("Erreur récupération véhicules :", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVehicules();
  }, []);

  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border text-primary"></div>
        <p className="mt-3">Chargement des véhicules...</p>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <h2 className="mb-4">🚗 Véhicules Disponibles</h2>
      <div className="row g-4">
        {vehicules.length === 0 && (
          <div className="alert alert-info text-center shadow-sm">
            Aucun véhicule disponible.
          </div>
        )}

        {vehicules.map((v) => (
          <div key={v.id} className="col-12 col-md-6 col-lg-4">
            <div className="card h-100 shadow-sm border-0">

              {/* Image */}
              {v.image_url && (
                <img
                  src={`http://localhost:8000${v.image_url}`}
                  alt={v.model}
                  className="card-img-top"
                  style={{ height: 180, objectFit: "cover" }}
                />
              )}

              <div className="card-body d-flex flex-column">
                <h5 className="card-title fw-bold">
                  {v.brand} {v.model} ({v.year})
                </h5>

                <p className="mb-1">
                  <strong>Prix :</strong> ${v.price.toLocaleString()}
                </p>

                <p className="mb-1">
                  <strong>Kilométrage :</strong> {v.kilometrage} km
                </p>

                <p className="mb-1">
                  <strong>Carburant :</strong> {v.carburant}
                </p>

                <p className="mb-1">
                  <strong>Transmission :</strong> {v.transmission}
                </p>

                <p className="mb-1">
                  <strong>Type :</strong> {v.type}
                </p>

                <p className="mb-2">
                  {v.description}
                </p>

                <span className={`badge ${v.available ? "bg-success" : "bg-danger"}`}>
                  {v.available ? "Disponible" : "Indisponible"}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Vehicules;