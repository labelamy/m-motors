import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Vehicules() {
  const [vehicules, setVehicules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [mesDossiers, setMesDossiers] = useState([]);
  const [filters, setFilters] = useState({
    type: "",
    carburant: "",
    maxPrice: ""
  });

  const navigate = useNavigate();

  const DEFAULT_IMAGE = "/seed_images/default_car.jpg";

  // 🔹 Récupérer dossiers
  const fetchDossiers = async () => {
    try {
      const res = await API.get("/dossiers/mes-dossiers");
      setMesDossiers(res.data);
    } catch (error) {
      console.error("Erreur dossiers :", error);
    }
  };

  // 🔹 Choisir véhicule
  const choisirVehicule = async (vehiculeId) => {
    try {
      await API.post("/dossiers/", {
        vehicule_id: vehiculeId,
        type: "achat",
      });
      alert("Véhicule choisi ✅");
      await fetchDossiers();
      navigate("/dossiers");
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Erreur ❌");
    }
  };

  // 🔹 Récupérer véhicules
  const fetchVehicules = async () => {
    try {
      const res = await API.get("/vehicules/");
      setVehicules(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const vehiculeDejaChoisi = (id) =>
    mesDossiers.some((d) => d.vehicule_id === id);

  useEffect(() => {
    fetchVehicules();
    fetchDossiers();
  }, []);

  // 🔍 FILTRAGE
  const filteredVehicules = vehicules.filter((v) => {
    return (
      (!filters.type || v.type.toLowerCase() === filters.type) &&
      (!filters.carburant || v.carburant === filters.carburant) &&
      (!filters.maxPrice || v.price <= filters.maxPrice)
    );
  });

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

      {/* 🔍 FILTRES */}
      <div className="row mb-4">
        <div className="col">
          <select
            className="form-select"
            onChange={(e) =>
              setFilters({ ...filters, type: e.target.value })
            }
          >
            <option value="">Type</option>
            <option value="achat">Achat</option>
            <option value="location">Location</option>
          </select>
        </div>

        <div className="col">
          <select
            className="form-select"
            onChange={(e) =>
              setFilters({ ...filters, carburant: e.target.value })
            }
          >
            <option value="">Carburant</option>
            <option>Essence</option>
            <option>Diesel</option>
            <option>Électrique</option>
          </select>
        </div>

        <div className="col">
          <input
            type="number"
            className="form-control"
            placeholder="Prix max"
            onChange={(e) =>
              setFilters({ ...filters, maxPrice: e.target.value })
            }
          />
        </div>
      </div>

      {/* 🚗 LISTE */}
      <div className="row g-4">
        {filteredVehicules.length === 0 && (
          <div className="alert alert-info text-center">
            Aucun véhicule trouvé.
          </div>
        )}

        {filteredVehicules.map((v) => {
          const imageSrc =
            v.image_url?.startsWith("http")
              ? v.image_url
              : v.image_url || DEFAULT_IMAGE;

        const isIndisponible = vehiculeDejaChoisi(v.id);      

          return (
            <div key={v.id} className="col-12 col-md-6 col-lg-4">
              
              <div
                className="card h-100 shadow-sm border-0"
                style={{ cursor: "pointer" }}
                onClick={() => navigate(`/vehicules/${v.id}`)}
              >
                <img
                  src={imageSrc}
                  alt={v.model}
                  className="card-img-top"
                  style={{ height: "220px", objectFit: "cover" }}
                  onError={(e) => {
                    e.target.src = DEFAULT_IMAGE;
                  }}
                />

                <div className="card-body d-flex flex-column">
                  <h5 className="fw-bold">
                    {v.brand} {v.model} ({v.year})
                  </h5>

                  <p><strong>Prix :</strong> {v.price.toLocaleString()} €</p>
                  <p><strong>Kilométrage :</strong> {v.kilometrage} km</p>
                  <p><strong>Carburant :</strong> {v.carburant}</p>
                  <p><strong>Transmission :</strong> {v.transmission}</p>
                  <p><strong>Type :</strong> {v.type}</p>
                  <p><strong>Description :</strong> {v.description}</p>

                  <div className="mt-auto d-flex justify-content-between align-items-center gap-2">

                  <span className={`badge ${isIndisponible ? "bg-danger" : "bg-success"}`}>
                    {isIndisponible ? "Indisponible" : "Disponible"}
                  </span>

                    <button
                      className={`btn btn-sm ${
                        isIndisponible ? "btn-secondary" : "btn-primary"}`}
                        disabled={isIndisponible}
                        onClick={(e) => {
                        e.stopPropagation();
                        choisirVehicule(v.id);}}>
                        {vehiculeDejaChoisi(v.id)
                        ? "Déjà choisi"
                        : isIndisponible
                        ? "Indisponible"
                        : "Choisir"}
                    </button>
                  </div>
                </div>

              </div>

            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Vehicules;