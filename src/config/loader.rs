//! Configuration Loader
//!
//! Handles loading and merging provider configurations from multiple sources.

use crate::config::provider::ProvidersConfig;
use crate::error::{LlmaoError, Result};
use std::collections::HashMap;
use std::path::{Path, PathBuf};

/// Configuration loader with support for multiple sources
pub struct ConfigLoader {
    /// Built-in provider registry (from providers.json)
    provider_registry: crate::config::provider::ProviderRegistry,
    /// User configuration (from config.json)
    config: ProvidersConfig,
}

impl ConfigLoader {
    /// Create a new config loader and load from default locations
    pub fn new() -> Result<Self> {
        let mut loader = Self {
            provider_registry: HashMap::new(),
            config: HashMap::new(),
        };

        // Load built-in provider registry first
        loader.load_provider_registry()?;

        // Then load user config from file system
        loader.load_from_default_paths()?;

        Ok(loader)
    }

    /// Create a loader with a specific config file
    pub fn from_path(path: impl AsRef<Path>) -> Result<Self> {
        let mut loader = Self {
            provider_registry: HashMap::new(),
            config: HashMap::new(),
        };

        loader.load_provider_registry()?;
        loader.load_from_file(path)?;

        Ok(loader)
    }

    /// Load built-in provider registry from providers.json
    fn load_provider_registry(&mut self) -> Result<()> {
        let defaults = include_str!("../../providers.json");
        let registry: crate::config::provider::ProviderRegistry = serde_json::from_str(defaults)
            .map_err(|e| {
                LlmaoError::Config(format!("Failed to parse built-in providers.json: {}", e))
            })?;

        self.provider_registry = registry;
        Ok(())
    }

    /// Load configuration from default paths
    fn load_from_default_paths(&mut self) -> Result<()> {
        let paths = Self::get_config_paths();

        for path in paths {
            if path.exists() {
                self.load_from_file(&path)?;
            }
        }

        Ok(())
    }

    /// Get list of config paths to check
    fn get_config_paths() -> Vec<PathBuf> {
        let mut paths = Vec::new();

        // 1. Environment variable
        if let Ok(custom_path) = std::env::var("LLMAO_PROVIDERS_PATH") {
            paths.push(PathBuf::from(custom_path));
        }

        // 2. Current directory
        paths.push(PathBuf::from("providers.json"));
        paths.push(PathBuf::from("llmao.json"));

        // 3. User config directory
        if let Some(config_dir) = dirs::config_dir() {
            paths.push(config_dir.join("llmao").join("providers.json"));
        }

        // 4. Home directory
        if let Some(home_dir) = dirs::home_dir() {
            paths.push(home_dir.join(".llmao").join("providers.json"));
        }

        paths
    }

    /// Load configuration from a specific file
    fn load_from_file(&mut self, path: impl AsRef<Path>) -> Result<()> {
        let path = path.as_ref();
        let content = std::fs::read_to_string(path)
            .map_err(|e| LlmaoError::Config(format!("Failed to read {}: {}", path.display(), e)))?;

        let config: ProvidersConfig = serde_json::from_str(&content).map_err(|e| {
            LlmaoError::Config(format!("Failed to parse {}: {}", path.display(), e))
        })?;

        self.merge_config(config);
        Ok(())
    }

    /// Merge another config into this one (later configs override earlier)
    fn merge_config(&mut self, other: ProvidersConfig) {
        for (key, config) in other {
            self.config.insert(key, config);
        }
    }

    /// Get the loaded provider registry
    pub fn provider_registry(&self) -> &crate::config::provider::ProviderRegistry {
        &self.provider_registry
    }

    /// Get the loaded configuration
    pub fn config(&self) -> &ProvidersConfig {
        &self.config
    }

    /// Take ownership of the configuration
    pub fn into_config(self) -> ProvidersConfig {
        self.config
    }
}

impl Default for ConfigLoader {
    fn default() -> Self {
        Self::new().unwrap_or_else(|_| Self {
            provider_registry: HashMap::new(),
            config: HashMap::new(),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    #[test]
    fn test_load_builtin_defaults() {
        let loader = ConfigLoader::new().unwrap();
        // Should have loaded provider registry
        assert!(!loader.provider_registry().is_empty());
    }

    #[test]
    fn test_load_from_custom_file() {
        let mut file = NamedTempFile::new().unwrap();
        writeln!(
            file,
            r#"{{
                "custom_provider/model-v1": {{
                    "keys": ["test-key-123"],
                    "base_url": "https://custom.api.com/v1"
                }}
            }}"#
        )
        .unwrap();

        let loader = ConfigLoader::from_path(file.path()).unwrap();
        assert!(loader.config().contains_key("custom_provider/model-v1"));
    }

    #[test]
    fn test_merge_configs() {
        let mut loader = ConfigLoader::new().unwrap();
        let initial_count = loader.config().len();

        // Create a custom config that adds a new model
        let mut custom = HashMap::new();
        custom.insert(
            "new_provider/model-v1".to_string(),
            crate::config::provider::ModelConfig {
                keys: vec!["key1".to_string()],
                models: vec![],
                base_url: Some("https://new.api.com".to_string()),
                rotation_strategy: Default::default(),
                headers: HashMap::new(),
                param_mappings: HashMap::new(),
                rate_limit: None,
            },
        );

        loader.merge_config(custom);
        assert_eq!(loader.config().len(), initial_count + 1);
    }
}
