import io.github.httpbuilderng.http.HttpTask 
import com.optum.giraffle.tasks.*
import com.optum.giraffle.*

buildscript {
    this.dependencies{
        this.classpath("com.opencsv:opencsv:3.8")
    }
}

plugins {
    id("com.optum.giraffle") version "1.3.4.1"
    id("net.saliman.properties") version "1.5.1"
    id("io.github.http-builder-ng.http-plugin") version "0.1.1"
}

repositories {
    jcenter()
}

http { 
    config{
        it.request.setUri("${gHostUriType}://${gHost}:${gRestPort}")
        it.request.headers["Authorization"] = "Bearer ${tigergraph.token.get()}"
    }
}

val gsqlGraphname: String by project
val gHost: String by project
val gAdminUserName: String by project
val gAdminPassword: String by project
val gUserName: String by project
val gPassword: String by project
val gGraphName: String by project
val gClientVersion: String? by project
val gCertPath: String? by project
val gHostUriType: String by project
val gRestPort: String by project
val gSecret: String? by project


val grpSchema: String = "Tigergraph Schema"  
val schemaGroup: String = "Schema"
val loadingGroup: String = "Loading"
val queryGroup: String = "Query Tasks"

val tokenMap: LinkedHashMap<String, String> = linkedMapOf("graphname" to gGraphName)

tigergraph {
    adminPassword.set(gAdminPassword)
    adminUserName.set(gAdminUserName)
    graphName.set(gGraphName)
    password.set(gPassword)
    scriptDir.set(file("db_scripts"))
    serverName.set(gHost)
    tokens.set(tokenMap)
    uriScheme.set(UriScheme.HTTPS)
    userName.set(gUserName)
    gClientVersion?.let { // <4>
        gsqlClientVersion.set(it)
    }
    gCertPath?.let {
        caCert.set(it)
    }
    gSecret?.let {
        authSecret.set(it)
    }
    logDir.set(file("./logs"))
    caCert.set("./cert.txt") 
}


tasks {
    wrapper {
        gradleVersion = "6.0.1"
    }

    register<GsqlTask>("showSchema") {
        scriptCommand = "ls"
        group = schemaGroup
        description = "Run simple `ls` command to display vertices, edges, and jobs for current graph"
    }

    register<GsqlTask>("createSchema") {
        scriptPath = "schema/schema.gsql"
        useGlobal = true
        group = schemaGroup
        description = "Runs gsql to create a schema"
    }

    register<GsqlTask>("dropSchema") {
        scriptPath = "schema/drop.gsql"
        group = schemaGroup
        description = "Runs gsql to drop the database schema"
    }

    register<GsqlTask>("dropAll") {
        scriptCommand = "drop all"
        group = schemaGroup
        description = "Run simple `drop all` command to destroy everything!"
    }

    register<GsqlTask>("dropData") {
        scriptCommand = "CLEAR GRAPH STORE -HARD"
        group = schemaGroup
        description = "This drops all the data."
    }

    val getToken by registering(GsqlTokenTask::class){ 
        uriScheme.set(tigergraph.uriScheme.get())
        host.set(tigergraph.serverName.get())
        defaultPort.set(tigergraph.restPort.get())
    }

    register<GsqlTokenDeleteTask>("deleteToken") { }

    register<GsqlTask>("createLoadData"){
        scriptPath = "load/loadData.gsql" // Call the file you have the load job in.
        group = loadingGroup
        description = "Loads our data"
    }
    register<HttpTask>("loadData") {
        group = loadingGroup
        description = "Load data via the REST++ endpoint"
        post { httpConfig ->
            httpConfig.request.uri.setPath("/ddl/${gGraphName}")
            httpConfig.request.uri.setQuery(
            mapOf(
            "tag" to "loadData",
            "filename" to "f1",
            "sep" to ",",
            "eol" to "\n"
            )
            )
            httpConfig.request.setContentType("text/csv")
            val stream = File("data/Words.csv").inputStream() // If your data file was called anything else, you can change the File("").
            httpConfig.request.setBody(stream)
        }
    }

    register<GsqlTask>("createQuerySimilarArticles") {
        scriptPath = "query/similar.gsql"
        group = queryGroup
        description = "Creates a similar query"
    }

    register<HttpTask>("getVersion") {
        description = "Get the server version from Tigergraph"
        get {
            it.request.uri.setPath("/version")
            it.response.success { fs, x ->
                println(fs )
                println(x)
                println("Success")
            }
        }
    }

    /* You'll add your data loads and query creations here! */

    withType<HttpTask>().configureEach { // <6>
        dependsOn(getToken)
    }
}

val allCreateLoad by tasks.registering {
    group = loadingGroup
    description = "Creates all load rules -- as long as they start with \"createLoad\"."
}

allCreateLoad {
    dependsOn(provider {
        tasks.filter{ task -> task.name.startsWith("createLoad") }
    })
}

val allLoad by tasks.registering {
    group = loadingGroup
    description = "Load all data -- as long as start with \"load\"."
}

allLoad {
    dependsOn(provider{
        tasks.filter{ task -> task.name.startsWith("load")}
    })
}