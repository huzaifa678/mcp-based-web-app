resource "aws_secretsmanager_secret" "app_credentials" {
  name = "mcp-app-credentials"

}

data "external" "env" {
  program = ["bash", "${path.module}/parse_env.sh"]
}

resource "aws_secretsmanager_secret_version" "production_credentials_version" {
  secret_id = aws_secretsmanager_secret.app_credentials.id
  secret_string = jsonencode({
    OPENAI_API_KEY = data.external.env.result.OPENAI_API_KEY
    SECRET_KEY = data.external.env.result.SECRET_KEY
    ALGORITHM = data.external.env.result.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = data.external.env.result.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS = data.external.env.result.REFRESH_TOKEN_EXPIRE_DAYS
  })
}