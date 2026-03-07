import { useEffect, useState } from "react";
import API from "../services/api";

function AdminDashboard() {
  const [dossiers, setDossiers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("ALL");

  const fetchDossiers = async () => {
    try {
      const res = await API.get("/dossiers/");
      setDossiers(res.data);
    } catch (error) {
      console.error("Erreur chargement dossiers", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDossiers();
  }, []);

  const updateStatus = async (id, status) => {
    try {
      await API.put(`/dossiers/${id}/status/${status}`);
      fetchDossiers();
    } catch (error) {
      console.error("Erreur update status", error);
    }
  };

  const getBadge = (status) => {
    if (status === "VALIDE") return "bg-success";
    if (status === "REFUSE") return "bg-danger";
    return "bg-warning text-dark";
  };

  // Statistiques
  const total = dossiers.length;
  const valides = dossiers.filter(d => d.status === "VALIDE").length;
  const refuses = dossiers.filter(d => d.status === "REFUSE").length;
  const attente = dossiers.filter(d => d.status === "EN_ATTENTE").length;

  // Filtre + recherche
  const filteredDossiers = dossiers
    .filter(d => d.id.toString().includes(search))
    .filter(d => filterStatus === "ALL" ? true : d.status === filterStatus);

  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border text-primary"></div>
        <p className="mt-3">Chargement des dossiers...</p>
      </div>
    );
  }

  return (
    <div className="container mt-5">

      <h2 className="mb-4">Dashboard Administrateur</h2>

      {/* Statistiques */}
      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card text-center shadow-sm">
            <div className="card-body">
              <h5>Total</h5>
              <h3>{total}</h3>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center shadow-sm border-success">
            <div className="card-body">
              <h5>Validés</h5>
              <h3 className="text-success">{valides}</h3>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center shadow-sm border-danger">
            <div className="card-body">
              <h5>Refusés</h5>
              <h3 className="text-danger">{refuses}</h3>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center shadow-sm border-warning">
            <div className="card-body">
              <h5>En attente</h5>
              <h3 className="text-warning">{attente}</h3>
            </div>
          </div>
        </div>
      </div>

      {/* Recherche + filtre */}
      <div className="row mb-4">
        <div className="col-md-6">
          <input
            type="text"
            className="form-control"
            placeholder="Rechercher un dossier par ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="col-md-3">
          <select
            className="form-select"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="ALL">Tous</option>
            <option value="EN_ATTENTE">En attente</option>
            <option value="VALIDE">Validé</option>
            <option value="REFUSE">Refusé</option>
          </select>
        </div>
      </div>

      {/* Tableau admin */}
      <div className="card shadow-sm">
        <div className="card-body">
          <table className="table table-hover align-middle">
            <thead className="table-dark">
              <tr>
                <th>ID</th>
                <th>Véhicule</th>
                <th>Status</th>
                <th>Document</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredDossiers.map((d) => (
                <tr key={d.id}>
                  <td>{d.id}</td>
                  <td className="d-flex align-items-center gap-2">
                    {d.vehicule?.image_url && (
                      <img
                        src={`http://localhost:8000${d.vehicule.image_url}`}
                        alt={d.vehicule.model}
                        style={{ width: 60, height: 40, objectFit: "cover", borderRadius: 4 }}
                      />
                    )}
                    <span>{d.vehicule?.brand} {d.vehicule?.model}</span>
                  </td>
                  <td>
                    <span className={`badge ${getBadge(d.status)}`}>
                      {d.status}
                    </span>
                  </td>
                  <td>
                    {d.document_path ? (
                      <a
                        href={`http://localhost:8000${d.document_path}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-sm btn-outline-primary"
                      >
                        Voir
                      </a>
                    ) : (
                      <span className="text-muted">Aucun</span>
                    )}
                  </td>
                  <td>
                    {d.status === "EN_ATTENTE" && (
                      <div className="d-flex gap-2">
                        <button
                          className="btn btn-success btn-sm"
                          onClick={() => updateStatus(d.id, "VALIDE")}
                        >
                          Valider
                        </button>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => updateStatus(d.id, "REFUSE")}
                        >
                          Refuser
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}

export default AdminDashboard;