'use strict'

module.exports = {
  service: 'General',
  provider: {
    name: 'aws',
    stage: 'prod',
    region: 'eu-north-1',
    runtime: "python3.12",
    logs: {
      // Enable CloudWatch logs
      restApi: true,
      lambda: {
        logFormat: "JSON"
      }
    },
    logRetentionInDays: 7 // Set log retention period
  },
  package: {
    patterns: ['!node_modules/**', '!venv/**', '!my-project**', '!package.json', '!package-lock.json', 'README.md']
  },
  functions: {
    proxyServer: {
      handler: "proxyServer.main",
      timeout: 30,
      name: `General-proxyServer`,
      memorySize: 512,
      description: "Proxies incoming http reguests with modifications.",
      logRetentionInDays: 7 // You can also set this at the function level
    }
  },
  plugins: ["serverless-python-requirements"],
  custom: {
    pythonRequirements: {
      useDownloadCache: false, //not using cache prevents broken dependencies
      useStaticCache: false //not using cache prevents broken dependencies
    }
  }
}



