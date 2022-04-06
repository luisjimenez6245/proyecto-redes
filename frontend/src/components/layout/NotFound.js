
function NotFound() {
    return (
        <section className={`hero is-fullheight-with-navbar `}>
            <div className="hero-body">
                <div className="container">
                    <div className="columns is-centered">
                        <div className="column is-6">
                            <div className="card">
                                <header class="card-header">
                                    <p className="card-header-title">
                                        ERROR 404
                                    </p>
                                </header>
                                <div className=" card-content ">
                                    <div className="field">
                                       
                                    </div>
                                    <div className="field py-3"></div>
                                    <div className="field is-grouped is-grouped-centered">
                                        <p className="control">
                                            <a
                                                className="button"
                                                href='/'
                                            >
                                                La página que buscas no fue encontrada.
                                            </a>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default NotFound