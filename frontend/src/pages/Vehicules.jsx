import { useEffect, useState } from "react";
import API from "../services/api";

function Vehicules() {
  const [vehicules, setVehicules] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVehicules = async () => {
      try {
        const response = await API.get("/vehicules/");
        setVehicules(response.data);
      } catch (error) {
        console.error("Erreur lors de la récupération des véhicules :", error);
      } finally {
        setLoading(false);
      }
    };

    fetchVehicules();
  }, []);

 const handleCreateDossier = async (vehiculeId) => {
    try {
      await API.post("/dossiers/", {
        vehicule_id: vehiculeId,
        type: "achat"
      });

      alert("Dossier créé avec succès !");
    } catch (error) {
      console.error(error);
      alert("Erreur lors de la création du dossier");
    }
  };

  if (loading) {
    return <p>Chargement des véhicules...</p>;
  }

  return (
    <div className="container mt-5">
      <h2>Liste des véhicules</h2>
      {vehicules.length === 0 ? (
        <p>Aucun véhicule disponible.</p>
      ) : (
        <div className="row">
          {vehicules.map((v) => (
            <div key={v.id} className="col-md-4 mb-3">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{v.brand} {v.model}</h5>
                  <p className="card-text">Type : {v.type}</p>
                  <p className="card-text">Prix : {v.price} €</p>
                  <p className="card-text">
                    {v.available ? "Disponible" : "Indisponible"}
                  </p>
                   <button
                    className="btn btn-primary mt-2"
                    onClick={() => handleCreateDossier(v.id)}>
                    Créer un dossier
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Vehicules;